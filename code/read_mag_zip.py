from zipfile import ZipFile

dir_path = "/mnt/ds3lab/yanping/mag"
#line_count = 0
with ZipFile(dir_path+"/data/mag_papers_0.zip", "r") as fin:
	while True:
		for i in range(10):
			line = fin.readline()
			if not line:
				print("***end of file***")
				break
			print(line)
		cont = input()
		if cont != "":
			break
