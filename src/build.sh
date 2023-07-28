#!/bin/sh

TM1_USERNAME="svc-epm-deploy-prod"
GROUP="OneLogin"

set -euo

shell_build1 () {
  #git checkout $GIT_SHA1;
  #find . -name connect.json -type f -exec sed -i 's/tm1dev.awscorp.uberinternal.com/test.tm1ext.awscorp.uberinternal.com/g' {} \;
  #find . -name connect.json -type f -exec sed -i 's/tm1uat.awscorp.uberinternal.com/uat.tm1ext.awscorp.uberinternal.com/g' {} \;
  #find . -name connect.json -type f -exec sed -i 's/tm1.awscorp.uberinternal.com/prod.tm1ext.awscorp.uberinternal.com/g' {} \;
  
  cat <<EOF > config/default/credentials.json
                {
    "namespace": "TM1_NAMESPACE",
    "user": "TM1_USERNAME",
    "password": "TM1_PASSWORD"
  }
EOF

  sed -i "s/TM1_NAMESPACE/$GROUP/g" config/default/credentials.json
  sed -i "s/TM1_USERNAME/$TM1_USERNAME@corp.uber.com/g" config/default/credentials.json
  sed -i "s/@corp.uber.com//g" config/default/credentials.json
  sed -i "s/TM1_PASSWORD/$TM1_PASSWORD/g" config/default/credentials.json
}


## This function can be removed as it's directly baked into the container
shell_build2 () {
  wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz;
  tar xvf Python-3.6.3.tgz
  cd Python-3.6.3
  ./configure --with-ensurepip=install --prefix=$HOME/.local;
  make -j8
  make altinstall
}



## This function can be removed as it's directly baked into the container
shell_build3 () {
  $HOME/.local/bin/pip3.6 install tm1cm[taptools] --upgrade
  echo "Done tm1cm installation .."
}


execute_tm1cm () {
  echo "Start tm1cm .."

  
  ## Uncomment below for the connectivity test
  # curl -Ivk https://pac.uat.tm1ext.awscorp.uberinternal.com:443/api/v1/Cubes --connect-timeout 30
  ## 

  /work/.local/bin/python3.6 -m tm1cm --mode put --environment ${TARGET_ENVIRONMENT} --path $(pwd)

  echo "End tm1cm .."

  # execute TI 
  execute_ti
  
  echo "End TI execution .."
  
}

execute_tm1cm_replica() {
  ## Get the current repo name
  repo_name=$(basename $(git remote get-url origin))

  if [ -s "$replica_connect_file" ]
  then 
    echo "$replica_connect_file file exists and is not empty. Proceeding ... "
  
    ## connect and replica-connect for the target env
    connect_file=$(find ./config/${TARGET_ENVIRONMENT} -type f -name connect.json)

    ## Get the current repo name
    repo_name=$(basename $(git remote get-url origin))

    ## Get the count of the json elements in replica json
    len=$(jq length $replica_connect_file)
    echo "Number of replica: $len"

    for i in $(seq 0 $(( $len - 1 ))); do
        ## Take backup of the connect.json
        cp  ${connect_file} ${connect_file}.$i
        
	      ## extract the replica json content
        echo "Connect json for Replica $(( $i + 1 )) is $(cat $replica_connect_file| jq .[$i])"
        extract_replica_address="cat $replica_connect_file| jq .[$i]"

  	    ## extract the replica name like analytics-1, planning-1
        extract_replica_name=$( cat $replica_connect_file| jq .[$i].address | tr -d '"' | awk -F '.' '{print $1}' )
        echo "replica instance name is $extract_replica_name"
        echo "primary instance name is $repo_name"

        ## Create connect.json file for the replica instance
        echo "Create replica ${connect_file} file"
        cat > ${connect_file} << EOF
$(eval $extract_replica_address)
EOF

        ## Find and replace the primary instance name with replica name in the ART python scripts
        echo "Find and Replace $repo_name with $extract_replica_name in ART Scripts"
        
        s1="source = \[\["\'$repo_name\'
        s2="source = \[\["\'$extract_replica_name\'
        find scripts/local/test_scripts -type f -name "*.py" -exec sed -i "s#$s1#$s2#g" {} \;

        t1="target = \[\["\'$repo_name\'
        t2="target = \[\["\'$extract_replica_name\'
        find scripts/local/test_scripts -type f -name "*.py" -exec sed -i "s#$t1#$t2#g" {} \;

        r1="\["\'$repo_name\'
        r2="\["\'$extract_replica_name\'
        find scripts/local/test_scripts -type f -name "*.py" -exec sed -i "s#$r1#$r2#g" {} \;

        grep "source = " scripts/local/test_scripts/*.py
        grep "target = " scripts/local/test_scripts/*.py
        
        repo_name=$extract_replica_name

        ## Run tm1cm command on the new connect.json file created
        shell_build1
        execute_tm1cm 
        
    done
  else
    echo "$replica_connect_file file does not exist, or is empty "
  fi

}

execute_ti () {
  # Run TI
  # password=$(cat config/default/credentials.json | jq -r '.password')
  auth_encode_base64=$(echo -n "$TM1_USERNAME:$TM1_PASSWORD:$GROUP" | base64)
  # echo $auth_encode_base64

  address=$(cat config/${TARGET_ENVIRONMENT}/connect.json | jq -r '.address')
  echo $address

  curl -kv --location --request POST "https://$address:443/api/v1/Processes('TAP.Call.Export Redudant Objects')/ibm.tm1.api.v1.Execute" \
  --header "Authorization: CAMNamespace $auth_encode_base64" --header 'Content-Type: application/json; charset=utf-8' 

  echo "End TI execution .."
}

### Main body of script starts here

## Enable debug
set -x

echo "Start of script..."

shell_build1
execute_tm1cm

### HA Implementation
## If replica file exists then execute the Replica function
replica_connect_file=$(find ./config/${TARGET_ENVIRONMENT} -type f -name replica-connect.json)
if [ -s "$replica_connect_file" ]
  then
    execute_tm1cm_replica
fi
### HA Implementation Done

echo "End of script..."

## Disable debug
set +x

### Main body of script ends here
