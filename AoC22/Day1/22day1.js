import { readFileSync } from "fs";
var text = readFileSync("./input.txt").toString('utf-8');
var textByLine = text.split("\n") 


//Split the input text by double line break, 
const elfCalories  = text
.split('\n\n')
.map(elf => {
    return elf
    .split('\n')
    .reduce((total, current) => total +Number(current.trim()),0);
})
.sort((a,b) => b-a);




console.log(elfCalories[0]);

