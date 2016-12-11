A= LOAD 's3://ngrams-english-mega/*' USING PigStorage('\t') AS (f1:chararray, f2:int, f3: float, f4: float);
B=FOREACH A GENERATE f1,f3,f4;
C= GROUP B BY f1;
D= FOREACH C GENERATE group,SUM(B.f3)/SUM(B.f4) AS f5;
E= ORDER D BY f5 DESC, group ASC;
F= LIMIT E 10; 
STORE F INTO 's3://cse6242-dawei/output' USING PigStorage('\t');
