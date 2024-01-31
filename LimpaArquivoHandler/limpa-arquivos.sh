#!/bin/bash

echo "Lista de arquivos marcados como \"deleted\" mas com handler aberto:"
lsof +L1 | awk '{print $1" - "$2" - "$4" - "$7" - "$10}'

printf "\n\n\nLimpando os arquivos:\n"
IFS=$'\n'; for i in `lsof +L1|tail --lines=+2`
do
  k=''
#  echo $i| awk '{print $1" - "$2" - "$4" - "$7" - "$10}'
  pid=`echo $i|awk '{print $2}'`
  fd=`echo $i|awk '{print $4}'`
  fn=`echo $i|awk '{print $10}'`
  printf "\nLimpar $fn? [s/N]"
  read k <&1
  if ! [[ $k = s ]] ; then
    : > /proc/$pid/fd/${fd::-1}
  fi
  sleep 5s
done

