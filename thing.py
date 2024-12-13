import boto3
import json
import random
import string
from pathlib import Path

thingArn = ''
thingId = ''
thingName = ''
# thingName = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
defaultPolicyName = 'My_Iot_Policy'
path = Path("./info")
if not path.exists():
    path.mkdir()

def createThing():
    global thingClient
    thingResponse = thingClient.create_thing(
        thingName = thingName
    )
    data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
    for element in data: 
        if element == 'thingArn':
            thingArn = data['thingArn']
        elif element == 'thingId':
            thingId = data['thingId']
            createCertificate()

def createCertificate():
        global thingClient
        certResponse = thingClient.create_keys_and_certificate(
                setAsActive = True
        )
        data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
        for element in data: 
            if element == 'certificateArn':
                    certificateArn = data['certificateArn']
            elif element == 'keyPair':
                    PublicKey = data['keyPair']['PublicKey']
                    PrivateKey = data['keyPair']['PrivateKey']
            elif element == 'certificatePem':
                    certificatePem = data['certificatePem']
            elif element == 'certificateId':
                    certificateId = data['certificateId']
                             
        with (path / (thingName+'_public.key')).open('w') as outfile:
                outfile.write(PublicKey)
        with (path / (thingName+'_private.key')).open('w') as outfile:
                outfile.write(PrivateKey)
        with (path / (thingName+'_cert.pem')).open('w') as outfile:
                outfile.write(certificatePem)

        response = thingClient.attach_policy(
                policyName = defaultPolicyName,
                target = certificateArn
        )
        response = thingClient.attach_thing_principal(
                thingName = thingName,
                principal = certificateArn
        )
        response = thingClient.add_thing_to_thing_group(
            thingGroupName='My_Thing_Group',
            thingName=thingName
        )

thingClient = boto3.client('iot')
for i in range(15):
    thingName = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
    createThing()