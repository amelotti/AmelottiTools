#!/bin/bash
#

check_mysql()
{
  echo "teste"
}


check_inputs()
{
if [ -z "$1" ]
then
  echo "Não informou o DBUSER"
  exit
elif [ -z "$2" ]
then
  echo "Não informou o DBPASS"
  exit
elif [ -z "$3" ]
then
  echo "Não informou o DBHOST"
  exit
fi
}


dbreport()
{
  mysql -u $DBUSER -p$DBPASS -h $DBHOST --silent --skip-column-names --execute "select concat('\'',User,'\'@\'',Host,'\'') as User from mysql.user" | sort | \
  while read u
   do 
     echo "-- $u"; mysql -u $DBUSER -p$DBPASS -h $DBHOST --silent --skip-column-names --execute "show grants for $u" | sed 's/$/;/'
     echo "--"
  done >> db_users_report-$DBPASS-`date +%Y%m%d`.txt
}


### Main

while getopts u:p:h: param
do
  case "${param}"
  in
    u) DBUSER=${OPTARG};;
    p) DBPASS=${OPTARG};;
    h) DBHOST=${OPTARG};;
  esac
done

check_inputs $DBUSER $DBPASS $DBHOST
dbreport

echo "Relatorio concluido"
echo " "
