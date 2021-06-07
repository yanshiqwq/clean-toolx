import logging, json, os, sys, platform
from os.path import getsize
try:
	def convert_size(size):
		try:
			if size >= 1000:
				if size >= 1000*1000:
					if size >= 1000*1000*1000:
						if size >= 1000*1000*1000*1000:
							total_size = str(format(size / (1000*1000*1000*1000), ".2f")) + "TB"
						else:
							total_size = str(format(size / (1000*1000*1000), ".2f")) + "GB"
					else:
						total_size = str(format(size / (1000*1000), ".2f")) + "MB"
				else:
					total_size = str(format(size / 1000, ".2f")) + "KB"
			else:
				total_size = str(format(size, ".2f")) + "B"
		except OSError:
			logging.error("索引失败!")
			input()
			sys.exit()
		return total_size
	logging.basicConfig(level = logging.DEBUG,format = '[PID #%(process)d] [%(levelname)s] %(message)s')
	logger = logging.getLogger(__name__)
	print()
	print("    #==================================#")
	print("    |   clean-toolx v1.0 By @延时qwq   |")
	print("    #==================================#")
	print()
	if os.listdir("./plugins"):
		clean_size = 0
		for root,dirs,files in os.walk("./plugins"):
			for file in files:
				plugin_data = open("./plugins/" + file).read()
				try:
					plugin_config = json.loads(plugin_data)
				except json.decoder.JSONDecodeError as e:
					logging.error("插件配置有误!请检查插件完整性.")
					continue
				logging.info("插件名称: " + plugin_config["name"] + " (" + file + ")")
				logging.info("插件作者: " + plugin_config["author"])
				logging.info("插件版本: " + plugin_config["version_name"])
				if plugin_config["platform"] != platform.system().lower():
					logging.warn("此插件不适配此操作系统!")
					continue
				logging.info("正在索引文件...")
				for rule in plugin_config["rules"]:
					path_list = []
					total_size = 0
					for paths in rule["paths"]:
						for root,dirs,names in os.walk(paths["path"]):
							for filename in names:
								path_list.append(os.path.join(root,filename))
								total_size = total_size + getsize(os.path.join(root,filename))
					filecount = len(path_list)
					logging.info("检测到" + str(filecount) + "个文件(" + convert_size(total_size) + "):")
					count = 0
					for filepath in path_list:
						print("\t [" + convert_size(getsize(filepath)) + "]\t" + filepath)
						count = count + 1
						if count >= 10:
							print("\t  ......\t ......")
							break
					print("")
					if rule["warning_level"] == 1:
						logging.info("正在清理文件...")
						count = 1
						for file in path_list:
							try:
								filesize = getsize(file)
								os.remove(file)
							except PermissionError as e:
								if "[WinError 5]" in str(e):
									print("\t [" + str(count) + "/" + str(filecount) + "] \t拒绝访问 - " + file)
								if "[WinError 32]" in str(e):
									print("\t [" + str(count) + "/" + str(filecount) + "] \t删除失败 - " + file)
							else:
								print("\t [" + str(count) + "/" + str(filecount) + "] \t删除文件 - " + file)
								clean_size = clean_size + filesize
							count = count + 1
					print("")
				logging.info("清理完毕!\n")
			logging.info("清理了" + convert_size(clean_size) + "的文件.")
		logging.info("清理完毕!")
	else:
		logging.error("未检测到任何插件!")
except FileNotFoundError:
	pass