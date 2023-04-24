import xml.etree.ElementTree as ET
from xml.dom import minidom as MD
import re

log_file = "kselftest_output.log"
kself_testlist = "kselftest-list.txt"

def get_pass_fail_test(xml_tag, search_string, test_result):
    passed_regex = re.findall("^ok (\d+) {}$".format(search_string), test_result, re.MULTILINE)
    failed_regex = re.findall("^not ok (\d+) {}".format(search_string), test_result, re.MULTILINE)
    skipped_regex = re.findall("^ok (\d+) {} # SKIP".format(search_string), test_result, re.MULTILINE)

    for status in ["passed", "failed", "skipped"]:
        res = eval(status+"_regex")
        if xml_tag.find(status):
            tc_status = xml_tag.find(status)
            tc_status.text = str(int(tc_status.text) + len(res))
        else:
            ET.SubElement(xml_tag, status).text = str(len(res))


def get_test_case_summary(xml_tag, test_result):
    summary = ['0', '0', '0', '0', '0', '0']
    result_regex = re.search("Totals: pass:(\d+) fail:(\d+) xfail:(\d+) xpass:(\d+) skip:(\d+) error:(\d+)",
                             test_result)
    if result_regex:
        summary = result_regex.groups()
    ET.SubElement(xml_tag, "passed").text = summary[0]
    ET.SubElement(xml_tag, "failed").text = summary[1]
    ET.SubElement(xml_tag, "skipped").text = summary[4]
    ET.SubElement(xml_tag, "error").text = summary[5]


def analyze_kselftest_log():
    log_fd = open(log_file)
    log_contents = log_fd.read()
    test_fd = open(kself_testlist)
    root = ET.Element("KSelftest")
    for test in test_fd.readlines():
        test_suite = test.split(":")[0].strip()
        test_name = test.split(":")[1].strip()
        search_string = "selftests: /{0}: {1}".format(test_suite, test_name)
        test_log = re.search("{0}(.*{0}.......)".format(search_string), log_contents, re.DOTALL)
        if "/" in test_suite: test_suite = test_suite.replace("/", "_")
        if root.find(test_suite):
            tc_element = root.find(test_suite)
        else:
            tc_element = ET.SubElement(root, test_suite)
        tc_details = ET.SubElement(tc_element, test_name)
        test_result = "/n".join(test_log.groups())
        ET.SubElement(tc_details, "system-out").text = test_result
        get_test_case_summary(tc_details, test_result)
        get_pass_fail_test(tc_element, search_string, test_result)
    log_fd.close()
    test_fd.close()
    xml_content = ET.tostring(root, 'unicode', 'xml')
    return xml_content


kselftest_xml = analyze_kselftest_log()

reparsed = MD.parseString(kselftest_xml)
indent_data = reparsed.toprettyxml(indent="  ")
k_fd = open("kselftest.xml", "w")
k_fd.write(indent_data)
k_fd.close()

