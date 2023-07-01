from tcp_latency import measure_latency

x = measure_latency(host='94.68.80.49' , port=15001,runs = 10)

print(x)

sum = 0
for ping in x:
	sum += ping
	
avg = sum/10

print("avg",avg)

input()