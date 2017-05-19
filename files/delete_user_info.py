__author__ = 'zyu'
#gitlab api url:http://doc.gitlab.com/ce/api/
import urllib
import httplib
import json
import pymongo
import ldap

class GitLabUtil(object):
	@staticmethod
	def create_http_client(host, port, req, url, params):
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		http_client = httplib.HTTPConnection(host, port, timeout=30)
		http_client.request(req, url, params, headers)
		return http_client
		
	@staticmethod
	def handle_response(response):
		status = response.status
		if status == 200 or status == 201:
			return True, response.read()
		elif status == 400:
			output = ""
			message = json.loads(response.read())
			for key, value in message["message"].items():
				output = output + key + ": "
				for msg in value:
					output = output + msg + ", "
				output = output + ";"
			return False, output
		elif status == 403:
			return False, "403 Forbidden - The request is not allowed."
		elif status == 404:
			return False, "404 Not Found - The resource you asked could not be accessed or found."
		elif status == 409:
			return False, "409 Conflict - A conflicting resource already exists."
		elif status == 500:
			return False, "500 Server Error."
		else:
			return False, response.reason
			
	#user log in by shibboleth,so we cannot get private_token,so add function below
	@staticmethod
	def get_userid(host, port, admin_token, username):
		print "git.get_users"
		http_client = None
		try:
			url = "/api/v3/users?search={0}&&private_token={1}".format(username,admin_token)
			params = urllib.urlencode({})
			http_client = GitLabUtil.create_http_client(host, port, "GET", url, params)
			result, message = GitLabUtil.handle_response(http_client.getresponse())
		except Exception, e:
			print e
			result = False
			message = "Error in get_user function"
		finally:
			if http_client:
				http_client.close()
		message = json.loads(message)
		return result,message[0]
		
	@staticmethod
	def delete_git_account(host, port, admin_token, userid):
		print "git.create_account"
		http_client = None
		try:
			url = "/api/v3/users/" + str(user_id) + "/keys?private_token={0}".format(admin_token)
			params = urllib.urlencode({})
			http_client = GitLabUtil.create_http_client(host, port, "DELETE", url, params)
			result, message = GitLabUtil.handle_response(http_client.getresponse())
		except Exception, e:
			print e
			result = False
			message = "Error in create_account function"
		finally:
			if http_client:
				http_client.close()
		return result, message
		
def delete_ldap_account(username):
	try:
		#ldap_url = "ldap://10.9.17.245:389"
		ldap_url = "ldap://172.16.13.177:389"
		principal_name = "cn=admin,dc=edx,dc=com"
		ldap_password  = "p@ssw0rd"
		base_dn = "ou=Users,dc=edx,dc=com"
		l = ldap.initialize(ldap_url)
		l.bind(principal_name, ldap_password)
		deleteDN = ("cn=%s," + base_dn) % ldap_getcn(username)
		l.delete_s(deleteDN)
	except ldap.LDAPError, e:
		print e
		
def delete_mongo_info(edx_host, port, mongo_admin, mongo_pwd, email, username):
	conn = pymongo.Connection(edx_host, port)
	db = conn.test
	db.authenticate(mongo_admin, mongo_pwd)
	db.ibm.remove({"email":email})
	db.token.remove({"username":username})
	
if __name__ == '__main__':
	#config of host and port
	edx_host = '172.16.14.147'
	mongo_port = 27017
	git_host = '172.16.13.236'
	git_admin_token = '9b7YDTxPuN9-ztwchRJ2'
	mongo_admin = 'edxapp'
	mongo_pwd = 'p@ssw0rd'
	email = sys.argv[1]
	git_user_name = sys.argv[2]
	edx_user_name = sys.argv[3]
	ldap_name = sys.argv[4]
	
	print email + " ;" + git_user_name + " ;" + edx_user_name + " ;" + ldap_name
	
	print "start delete ldap account..."
	delete_ldap_account(ldap_username)
	
	print "start delete gitlab account..."
	result,userid = GitLabUtil.get_userid(git_host, 80, git_admin_token, git_user_name)
	if result == False:
		print "failed get userid, does user exist? " + message
	else:
		print "user id: " + userid
	result,message = GitLabUtil.delete_git_account(git_host, 80, git_admin_token, userid)
	if result == False:
		print "failed delete account," + message
	else:
		print "success!"
		
	print "start empty user info in mongodb..."
	delete_mongo_info(edx_host, mongo_port, mongo_admin, mongo_pwd, email, edx_username)
	print "success!"
	
	#email = "test@example.com"
	#result,message= GitLabUtil.add_ssh_key('172.16.13.236', 80, admin_token,import_url,"test project",user_id)
	#print result,message
