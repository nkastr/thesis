# file running locust files for stressing applications

# define file to run and host ip
file="./locust-eshop.py"
host="35.205.155.74:80"

# run locust
python3 -m locust -f ${file} --host "http://"${host} --users 500 --spawn-rate 20 