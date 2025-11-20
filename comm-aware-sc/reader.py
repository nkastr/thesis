import os
import re
import yaml


def addNodeSelector(path, name, node):        # node has to be labeled w/ name=NODE_NAME
    path = path + name + ".yaml"
    body = []
    with open(path, 'r') as stream:
        body.append(list(yaml.load_all(stream, Loader=yaml.FullLoader)))
    body = body[0][0]

    body.get("spec").get("template").get("spec").update({"nodeSelector":{"name":node}}) 

    with open(path, 'w') as stream:
        yaml.dump(body, stream)


# for testing
# addNodeSelector("./my-thesis/comm-aware-sc/manifests/eshop/deployments/adservice", "edge1")

# reads a single yaml file
def readYaml(path, file):
    file = file + ".yaml"
    file = os.path.join(path, file)
    print("FILE:" + file)
    body = []
    if os.path.isfile(file):
        with open(file, 'r') as stream:
            body.append(list(yaml.load_all(stream, Loader=yaml.FullLoader)))

    return body

# reads all yamls in a directory (read multiple yaml)
def readMulYaml(path):
    loaded_data = []
    for filename in os.listdir(path):
        _, extension = os.path.splitext(filename)
        # print(filename, extension)
        if extension == ".yaml" or extension == ".yml":
            # print(filename, extension)
            file = os.path.join(path, filename)
            if os.path.isfile(file):
                with open(file, 'r') as stream:
                    loaded_data.append(
                        list(yaml.load_all(stream, Loader=yaml.FullLoader)))
    return loaded_data

def getDeploymentResources(path, file):   # pass empty string in file to read all yamls in dir
    requests = {}
    limits = {}
    if file:
        data = readYaml(path, file)
    else:
        data = readMulYaml(path)

    for docs in data:
        for doc in docs:
            if doc["kind"] == "Deployment":
                name = doc["metadata"]["name"]
                try:
                    temp = doc["spec"]["template"]["spec"]["containers"][0]["resources"]
                    requests[name] = temp["requests"]
                    limits[name] = temp["limits"]
                except:
                    requests[name] = {'cpu': "0", 'memory': "0"}
                    limits[name] = {'cpu': "0", 'memory': "0"}

    for data, values in requests.items():
        for k, v in values.items():
            tmp = re.findall('[0-9]+', v)[0]
            values[k] = int(tmp)

    for data, values in limits.items():
        for k, v in values.items():
            tmp = re.findall('[0-9]+', v)[0]
            values[k] = int(tmp)
    return requests, limits


# req, lim = getDeploymentResources("./my-thesis/comm-aware-sc/manifests/eshop/deployments/", "frontend-external")
# print(lim)

# def test():
#     body = readYaml("/home/nick/Desktop/thesis/related_thesis/prountzos_thesis/thanasis_thesis/my-thesis/comm-aware-sc/manifests/eshop/deployments/", "adservice")

#     for item in body[0]:
#         print(item)

# test()

# body = readYaml("/my-thesis/comm-aware-sc/manifests/eshop/deployments/", "checkoutservice")
# print(body)