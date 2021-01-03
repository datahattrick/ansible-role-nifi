import nipyapi
import argparse
import json
from jinja2 import Template

class CreatePrometheus:

    def __init__(self):
        # Declare all of the variables
        parser = argparse.ArgumentParser(description="Create a prometheus reporting task automatically in a nifi")
        parser.add_argument("-H","--hostname", action="store", help="hostname of the nifi instance", default="localhost")
        parser.add_argument("-P","--port", action="store", help="port of the nifi instance", default="8080")
        parser.add_argument("--prometheus-port", action="store", help="The Port where prometheus metrics can be accessed", default="9092")
        parser.add_argument("--prometheus-host", action="store", help="Id of this NiFi instance to be included in the metrics sent to Prometheus. (This is nifi expression language)", default="${hostname(true)}")
        parser.add_argument("--prometheus-strategy", action="store",choices=['All Components','All Process Groups','Root Process Group'], help="The granularity on which to report metrics.", default="All Components")
        parser.add_argument("--prometheus-jvm", action="store_true", help="Send JVM metrics in addition to the NiFi metrics", default='true')
        parser.add_argument("--prometheus-secure", action="store_true", help="If the nifi is secure, attempt to attach itself to a ssl context service", default=False)
        args = parser.parse_args()

        self.nifi_hostname = args.hostname
        self.nifi_port = args.port
        self.nifi_promethues_report_port = args.prometheus_port
        self.nifi_prometheus_report_host = args.prometheus_host
        self.nifi_prometheus_report_strategy = args.prometheus_strategy
        self.nifi_prometheus_report_send_jvm = args.prometheus_jvm
        self.nifi_is_secure = args.prometheus_secure
        self.existingReportTaskid = ''

        self.create_prometheus_body = {
            "revision": {
                "clientId": "0",
                "version": 0
            },
            "disconnectedNodeAcknowledged": False,
            "component": {
                "type": "org.apache.nifi.reporting.prometheus.PrometheusReportingTask",
                "bundle": {
                    "group": "org.apache.nifi",
                    "artifact": "nifi-prometheus-nar",
                    "version": "1.12.1"
                }
            }
        }

    def create_templates(self, id):
        modify_promtheus_body_tmp = Template('''{
            "component": {
                "id": "{{ nifi_prometheus_report_id }}",
                "name": "PrometheusReportingTask",
                "schedulingStrategy": "TIMER_DRIVEN",
                "schedulingPeriod": "60 sec",
                "comments": "automatically created",
                "state": "RUNNING",
                "properties": {
                    "prometheus-reporting-task-metrics-endpoint-port": "{{ nifi_promethues_report_port | default('9092') }}",
                    "prometheus-reporting-task-instance-id": "{{ nifi_prometheus_report_host | default('${hostname(true)}') }}",
                    "prometheus-reporting-task-metrics-strategy": "{{ nifi_prometheus_report_strategy | default('All Components') }}",
                    "prometheus-reporting-task-metrics-send-jvm": "{{ nifi_prometheus_report_send_jvm | default('true') | lower}}",
                    {% if nifi_is_secure -%}
                    "prometheus-reporting-task-ssl-context": "{{ nifi_secure_ssl_context_service }}",
                    "prometheus-reporting-task-client-auth": "{{ nifi_prometheus_report_task_client_auth | default('Need Authentication') }}"
                    {% else -%}
                    "prometheus-reporting-task-client-auth": "No Authentication"
                    {% endif -%}
                }
            },
            "revision": {
                "clientId": "0",
                "version": 2
            },
            "disconnectedNodeAcknowledged": false
        }''')
        modify_promtheus_body = modify_promtheus_body_tmp.render(nifi_prometheus_report_id=id,nifi_promethues_report_port=self.nifi_promethues_report_port,nifi_prometheus_report_host=self.nifi_prometheus_report_host,nifi_prometheus_report_strategy=self.nifi_prometheus_report_strategy,nifi_prometheus_report_send_jvm=self.nifi_prometheus_report_send_jvm,nifi_is_secure=self.nifi_is_secure)
        return json.loads(modify_promtheus_body)

    def initialise_api_connections(self):
        self.flowAPI = nipyapi.nifi.apis.flow_api.FlowApi()
        self.controllerAPI = nipyapi.nifi.apis.controller_api.ControllerApi()
        self.reportingTaskAPI = nipyapi.nifi.apis.reporting_tasks_api.ReportingTasksApi()

    def create_report_task(self):
        reportTasks = self.flowAPI.get_reporting_tasks().to_dict()
        listOfReportTasks = reportTasks['reporting_tasks']

        # Check to make sure if a prometheus report task already exists don't make another one.
        print("Checking for any existing prometheus report tasks...")
        for reportTask in listOfReportTasks:
            if 'org.apache.nifi.reporting.prometheus.PrometheusReportingTask' in reportTask['component']['type']:
                self.existingReportTaskid = reportTask['component']['id']

        if self.existingReportTaskid == '':

            print("Attempting to create a prometheus report task...")

            # if there is no reporting task for promethues create one.
            newReportTask = self.controllerAPI.create_reporting_task(self.create_prometheus_body).to_dict()
            reportTaskID = newReportTask['id']

            # Create the templates for the http body.
            modify_task_body = self.create_templates(reportTaskID)
            # Modify Settings and start the task.
            self.reportingTaskAPI.update_reporting_task(reportTaskID,modify_task_body)
            print("Created prometheus reporting task!")
        else:
            print("Stopping... A prometheus report task already exists")

    def connect_nifi(self):
        if self.nifi_is_secure == True:
            nipyapi.config.nifi_config.host = 'https://' + self.nifi_hostname + ':' + self.nifi_port + '/nifi-api'
        else:
            nipyapi.config.nifi_config.host = 'http://' + self.nifi_hostname + ':' + self.nifi_port + '/nifi-api'
        print("Attempting to connect to nifi api")
        self.nifiRoot = nipyapi.canvas.get_root_pg_id()

    def create_prometheus_report_task(self):

        # Attempt the connection to the nifi API
        self.connect_nifi()

        # If the root id is returned then create the report task
        if self.nifiRoot != '':
            self.initialise_api_connections()
            self.create_report_task()



if __name__ == '__main__':
    cp = CreatePrometheus()
    cp.create_prometheus_report_task()