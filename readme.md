1. We have a master server: 89.58.40.109 
2. Server run commands: 
- locust --class-picker --master --master-bind-port=5557 -P 8081
- locust --class-picker --master --master-bind-port=5558 -P 8082
- locust --class-picker --master --master-bind-port=5559 -P 8083
3. Client run below commends to connect to different master server:
- locust --worker --master-host=89.58.40.109 --master-port=5557
- locust --worker --master-host=89.58.40.109 --master-port=5558
- locust --worker --master-host=89.58.40.109 --master-port=5559