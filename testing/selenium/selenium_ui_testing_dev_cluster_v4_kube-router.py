from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys

def add_anchor_node(pod_id,rack_id,node_id,rtr_id,node_ipv4):
    elem = driver.find_element(By.NAME,"pod_id")
    elem.send_keys(pod_id)
    elem = driver.find_element(By.NAME,"rack_id")
    elem.clear()
    elem.send_keys(rack_id)
    select = Select(driver.find_element(By.ID,'node_id'))
    select.select_by_visible_text(node_id)
    elem = driver.find_element(By.NAME,"rtr_id")
    elem.clear()
    elem.send_keys(rtr_id)
    elem = driver.find_element(By.NAME,"node_ipv4")
    elem.clear()
    elem.send_keys(node_ipv4)
    elem = driver.find_element(By.ID,"add_node")
    elem.click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID,"add_node")))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID,"add_node")))

def add_calico_ndoe(hostname, ip, rack_id):
    elem = driver.find_element(By.NAME,"hostname")
    elem.clear()
    elem.send_keys(hostname)
    elem = driver.find_element(By.NAME,"ip")
    elem.clear()
    elem.send_keys(ip)
    elem = driver.find_element(By.NAME,"rack_id")
    elem.clear()
    elem.send_keys(rack_id)
    elem = driver.find_element(By.ID,"add_node")
    elem.click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID,"add_node")))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID,"add_node")))

def wait_for_title(driver, title):
    WebDriverWait(driver, 30).until(lambda x: title in x.title )

chrome_options = Options()
if len(sys.argv)>=2:
    port= sys.argv[1]
    chrome_options.add_argument(sys.argv[1])
driver = webdriver.Chrome(options=chrome_options)

driver.get("http://10.67.185.120:5002")
assert "NKT" in driver.title
elem = driver.find_element(By.NAME,"button")
elem.click()
wait_for_title(driver, "Apic Login")
elem = driver.find_element(By.NAME,"fabric")
elem.clear()
elem.send_keys("fab2-apic1.cam.ciscolabs.com")
elem = driver.find_element(By.NAME,"username")
elem.clear()
elem.send_keys("admin")
elem = driver.find_element(By.NAME,"password")
elem.clear()
elem.send_keys("123Cisco123")
elem = driver.find_element(By.ID,"submit")
elem.click()
#Wait for the page to be loaded
wait_for_title(driver, "L3OUT")

elem = driver.find_element(By.ID,'l3out_tenant')
elem.send_keys("kube-router")
elem = driver.find_element(By.NAME,"ipv4_cluster_subnet")
elem.clear()
elem.send_keys("192.168.43.0/24")
# WAIT FOR THE vrf_name_list TO BE POPULATED WITH AT LEAST 2 ELEMENTs (The first one is just the palce holder)
# THAT SHOULD BE ALL IT TAKES TO HAVE THE REST OF THE PAGE READY...
try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="vrf_name_list"]/option[2]')))
except ValueError as e:
    print("Loading took too much time!")

elem = driver.find_element(By.ID,'vrf_name')
elem.send_keys("kube-router/k8s")
elem = driver.find_element(By.ID,'contract')
elem.send_keys("common/kube-router")
elem = driver.find_element(By.ID,'physical_dom')
elem.send_keys("Fab2")

add_anchor_node("1","1","201","1.1.1.101","192.168.43.101")
add_anchor_node("1","1","202","1.1.1.102","192.168.43.102/24")
add_anchor_node("1","2","203","1.1.1.103","192.168.43.103")
add_anchor_node("1","2","204","1.1.1.104","192.168.43.104/24")

elem = driver.find_element(By.ID,"submit")
elem.click()

#Wait for the page to be loaded
wait_for_title(driver, "vCenter Login" )
elem = driver.find_element(By.NAME,"url")
elem.send_keys("vc2.cam.ciscolabs.com")
elem = driver.find_element(By.NAME,"username")
elem.send_keys("administrator@vsphere.local")
elem = driver.find_element(By.NAME,"pass")
elem.send_keys("123Cisco123!")
elem = driver.find_element(By.ID,"template_checkbox")
elem.click()
elem = driver.find_element(By.ID,"submit")
elem.click()

#Wait for the page to be loaded
wait_for_title(driver, "vCenter Details")
select = Select(driver.find_element(By.ID,'dc'))
select.select_by_visible_text("STLD")

#Wait for vCenter API to populate the page
try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="vms_list"]/option[1]')))
except ValueError as e:
    print("Loading took too much time!")

select = Select(driver.find_element(By.ID,'cluster'))
select.select_by_visible_text("Cluster")
elem = driver.find_element(By.ID,'port_group')
elem.send_keys("ACI/kube-router/vlan-103")
elem = driver.find_element(By.ID,'vm_templates')
elem.send_keys("nkt_template")
elem = driver.find_element(By.ID,'vm_folder')
elem.send_keys("kube-router")
elem = driver.find_element(By.ID,"submit")
elem.click()

#Wait for the page to be loaded
wait_for_title(driver, "Calico Nodes")
elem = driver.find_element(By.ID,'calico_nodes')
elem.clear()
add_calico_ndoe('gitaction-nkt-master-1','192.168.43.1/24', '1')
add_calico_ndoe('gitaction-nkt-master-2','192.168.43.2/24', '1')
add_calico_ndoe('gitaction-nkt-master-3','192.168.43.3/24', '1')
add_calico_ndoe('gitaction-nkt-worker-1','192.168.43.4/24', '1')
add_calico_ndoe('gitaction-nkt-worker-2','192.168.43.5/24', '1')
add_calico_ndoe('gitaction-nkt-worker-3','192.168.43.6/24', '1')


elem = driver.find_element(By.ID,"submit")
elem.click()

#Wait for the page to be loaded
wait_for_title(driver, "Cluster")
elem = driver.find_element(By.ID,'advanced')
elem.click()
elem = driver.find_element(By.ID,'timezone')
elem.send_keys("Australia/Sydney")
elem = driver.find_element(By.NAME,"dns_servers")
elem.send_keys("10.67.185.100")
elem = driver.find_element(By.NAME,"dns_domain")
elem.send_keys("cam.ciscolabs.com")
elem = driver.find_element(By.ID,'docker_mirror')
elem.send_keys("10.67.185.120:5000")
elem = driver.find_element(By.ID,'ntp_server')
elem.send_keys("72.163.32.44")
elem = driver.find_element(By.ID,'ubuntu_apt_mirror')
elem.send_keys("ubuntu.mirror.digitalpacific.com.au/archive/")
elem = driver.find_element(By.ID,"submit")
elem.click()

wait_for_title(driver, "Cluster Network")
elem = driver.find_element(By.ID,'cni_plugin')
elem.clear()
elem.send_keys("Kube-Router")
elem = driver.find_element(By.ID,"submit")

elem.click()
