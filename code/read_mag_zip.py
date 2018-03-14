from zipfile import ZipFile

dir_path = "/mnt/ds3lab/yanping/mag"
#line_count = 0
with ZipFile(dir_path+"/data/mag_papers_0.zip", "r") as myzip:
	zip_files = myzip.namelist()
	for file_name in zip_files:
		with myzip.open(file_name) as fin:
			print("***reading",file_name,"***")
			while True:
				for i in range(1):
					line = fin.readline()
					if not line:
						print("***end of",file_name,"***")
						break
					print(line)
				cont = input()
				if cont != "":
					exit()
