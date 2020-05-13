#!/usr/bin/env bash

[[ -z ${SPARK_HOME} ]] && SPARK_HOME='/root/.sdkman/candidates/spark/current'

echo """
usage:  sh dc-spark-submit.sh --conf key=value spark/spark_sql_guide.py
"""

container_name="spark-standalone"
docker_container_id=$(docker ps -a --format "table {{.ID}} {{.Names}}\t.Image}}\t{{.Status}}" | grep ${container_name} | cut -d ' ' -f 1)

[[ -z ${docker_container_id} ]] && echo "spark master container don't run succcess, please check it exit" && exit 1

# 分离最后一个py脚本路径参数
declare -i last=$#-1
py_script_file_path=${!#}
py_filename=${py_script_file_path##*/}

## 复制本地的文件的到容器 tmp 目录下
#docker cp ${py_script_file_path} ${docker_container_id}:/tmp/

# 容器内脚本挂载路径
#pyspark_script_prefix=/spark


# 容器内提交 pyspark
docker exec -it ${docker_container_id} ${SPARK_HOME}/bin/spark-submit --master spark://${docker_container_id}:7077 ${@:1:last} /${py_script_file_path}

## 删除容器内的文件
#docker exec -it ${docker_container_id} rm -rf /tmp/${py_filename}