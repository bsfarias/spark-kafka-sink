# SPARK KAFKA SINK

## Introdução
O objetivo do projeto é explorar o módulo structured streaming do Apache Spark e replicar eventos de um tópico kafka para outro.

##  Descrição
O arquivo utilizado para o teste é o `pageviews.txt` e contém dados fake.
Para a replicação, um job spark foi desenvolvido para replicar os eventos do tópico pageviews para o tópico pageviews-mirror. Neste exemplo, o módulo de [streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#output-sinks) foi explorado.

## Pré-requisitos:
* [docker](https://www.docker.com/products/docker-desktop)

## Construção do ambiente através do docker compose:
   - No terminal, execute o seguinte comando:
```
cd spark-kafka-sink/docker/
docker-compose up
```   

## Criação dos tópicos:
   - Acesse o container do kafka, crie os tópicos pageviews e pageviews-mirror e carregue dados do arquivo `pageviews.txt` no primeiro:
```
docker exec -i -t kafka_confluent /bin/bash

kafka-topics --create \
--bootstrap-server kafka_confluent:9094 \
--replication-factor 1 \
--partitions 1 \
--topic pageviews

kafka-topics --create \
  --bootstrap-server kafka_confluent:9094 \
  --replication-factor 1 \
  --partitions 1 \
  --topic pageviews-mirror

kafka-console-producer \
  --broker-list kafka_confluent:9094 \
  --topic pageviews < /home/appuser/pageviews.txt  
```

## Execução do job spark streaming:
   - Em outro terminal, acesse o container do spark e faça o submit do job:
```
docker exec -i -t spark-streaming /bin/bash

spark-submit --master local[*] \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 \
 /home/jovyan/scripts/kafka_sink.py
```

## Validação do tópico pageviews-mirror:
   - Acesse novamente o container do kafka e valide se os dados foram recplicados para o tópico pageviews-mirror:
```
docker exec -i -t kafka_confluent /bin/bash

kafka-console-consumer \
  --bootstrap-server kafka_confluent:9094 \
  --topic pageviews-mirror --from-beginning
```