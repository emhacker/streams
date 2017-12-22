#! /bin/bash
if [[ $# != 1 ]] ; then
    echo "Usage: run_example.sh <calculator|eratosthenes>"
    exit 1
fi
case $1 in
"calculator")
    PYTHONPATH=../../ python calculator.py
    ;;
"eratosthenes")
    PYTHONPATH=../../ python eratosthenes_sieve.py
    ;;
*)
    echo "No shuch example $1"
esac
