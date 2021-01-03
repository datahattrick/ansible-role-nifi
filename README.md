Apache Nifi
=========

Create an Apache Nifi server or cluster.
For more information about Nifi:
+ https://nifi.apache.org/
+ https://github.com/apache/nifi

This role was based on https://github.com/Asymmetrik/ansible-role-nifi 

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main/main.yml)

The variables are divided up into separate files to make it simpler in understanding what variables are available outside of the initial config.

### Default/main/main.yml

The default variable file will be able  create a instance of Nifi on its own so if you wish to have a simple nifi, simply follow the example playbook below.

#### **Base install config**

| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_install_java | bool | true | Nifi requires java 8 to be installed to run, this ansible role will install openJDK 8 unless otherwise specified. |
| nifi_check_install | bool | true | To help save space the removal of the initial archive binaries are required, to ensure it does not re-download the binaries, the role will check to see if Nifi is already installed.
| **nifi_version** | version | 1.12.1 | The version of Nifi to install from Apache Nifi. **Only required for remote install.** **Currently only set up for 1.12.1** |
| nifi_install_local | bool | false | Install Nifi from a local binary. |
| nifi_install_local_dir | directory | ./files/nifi-{{ nifi_version }}-bin.tar.gz | Location of the local binary. |
| nifi_base_dir | directory | /opt | Location of the base directory to install Nifi directories and files. |


#### **JVM Settings**

| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_memory_low | int | 512 | The initial and minimum heap size. |
| nifi_memory_high | int | 4096 | The maximum heap size. |

#### **Directory Locations**
| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_temp_file | directory | /tmp/nifi-{{ nifi_version }}-bin.tar.gz | Where to send the binaries when downloading before unarchiving. |
| nifi_etc_dir | directory | /etc/nifi | The etc directory, currently used to store local state management for the server. |
| nifi_log_dir | directory | /var/log/nifi | Location to store Nifi logs. |
| nifi_pid_dir | directory | /var/run/nifi | The PID file location for the systemd service. |
| nifi_nar_library_autoload_directory | directory | {{ nifi_home }}/extensions | Nifi nar directory to load in. |
| nifi_database_repository | directory | {{ nifi_home }}/database_repository | Nifi H2 database location. |
| nifi_flowfile_repository | directory | {{ nifi_home }}/flowfile_repository | Nifi Flowfile repository location |
| nifi_content_repositories | list | [ "{{ nifi_home }}/content_repository" ] | A list of content repository locations |
| nifi_provenance_ repositories | list | [ "{{ nifi_home }}/provenance_repository" ] | A list of provenance repository locations |

#### **Core properties**
| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_auto_resume_processors | bool | true | When Nifi restarts ensure that all processors that were active previously are turned back on. |
| nifi_default_backpressure_count | int | 10000 | The default backpressure amount of files for connections before backpressure begins. |
| nifi_default_backpressure_size | string | 1 GB | The default backpressure size allowed in a connection before backpressure begins. |
| nifi_banner_text | string | | The banner text to display on the web interface. |
| nifi_graceful_shutdown | int | 20 | How long to wait after telling NiFi to shutdown before explicitly killing the Process. |

#### **Flowfile Repository Properties**
| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_queue_swap_threshold | int | 20000 | When the number of FlowFiles exceeds the number of the configuration property “nifi.queue.swap.threshold” NiFi writes the FlowFiles with the lowest priority in the queue to a swap file on the disk in batches of 10,000. |

#### **Content Repository Properties**
| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_content_repo_insync | bool | false | If set to true, any change to the repository will be synchronized to the disk, meaning that NiFi will ask the operating system not to cache the information. |

#### **Archive Properties**
| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_archive_enabled | bool | false | Write and Archive the data the comes through Nifi, this allows for the ability to replay files after leaving the system. |
| nifi_archive_retention_period | string | 7 days | The total time that data is retained in the archive. |
| nifi_archive_usage_percentage | percentage | 50% | How much disk can the archive use before removing the oldest stored. |

#### **Provenance Properties**
| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_provenance_storage_time | string | 30 days | The maximum amount of time to keep data provenance information. |
| nifi_provenance_storage_size | string | 10 GB | The maximum amount of data provenance information to store at a time. For production environments, values of 1-2 TB or more is not uncommon. |
| nifi_provenance_rollover_time | string | 10 mins | The amount of time to wait before rolling over the "event file" that the repository is writing to. |
| nifi_provenance_rollover_size | string | 100 MB | The amount of data to write to a single "event file." For production environments where a very large amount of Data Provenance is generated, a value of 1 GB is also very reasonable. |
| nifi_provenance_query_threads | int | 2 | The number of threads to use for Provenance Repository queries. |
| nifi_provenance_index_threads | int | 2 | The number of threads to use for indexing Provenance events so that they are searchable. |
| nifi_provenance_indexed_fields | list | EventType, FlowFileUUID, Filename, ProcessorID, Relationship | This is a comma-separated list of the fields that should be indexed and made searchable. Fields that are not indexed will not be searchable. Valid fields are: EventType, FlowFileUUID, Filename, TransitURI, ProcessorID, AlternateIdentifierURI, Relationship, Details. |
| nifi_provenance_indexed_attributes | list |  | This is a comma-separated list of FlowFile Attributes that should be indexed and made searchable. |
| nifi_provenance_indexed_shard_size | string | 500 MB | The repository uses Apache Lucene to performing indexing and searching capabilities. This value indicates how large a Lucene Index should become before the Repository starts writing to a new Index. |

#### **Site to Site Properties**
| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_remote_input_host | hostname |  | The host name that will be given out to clients to connect to this NiFi instance for Site-to-Site communication. By default, it is the value from `InetAddress.getLocalHost().getHostName().` |
| nifi_remote_input_port | int | 9445 | The remote input socket port for Site-to-Site communication. |
| nifi_remote_input_http_enabled | bool | true | Specifies whether HTTP Site-to-Site should be enabled on this host. |

#### **Web Properties**
| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_web_host | hostname |  | The HTTP host |
| nifi_web_http_port | int | 8080 | The HTTP Port |
| nifi_web_https_port | int | 8443 | The HTTPS Port |

#### **Proxy Properties**
| Variable | Type | Default | Description |
| -------- | :--: | ------- | ----------- |
| nifi_proxy_context_path | list |  | A comma separated list of allowed HTTP X-ProxyContextPath, X-Forwarded-Context, or X-Forwarded-Prefix header values to consider. |
| nifi_proxy_host | list |  | A comma separated list of allowed HTTP Host header values to consider when NiFi is running securely and will be receiving requests to a different host[:port] than it is bound to. |

Example Playbook
----------------

Create a nifi server:

    - name: Initialise a nifi.
      hosts: nifi
      become: yes

      roles:
         - ansible-role-nifi

License
-------

GNU General Public License v3.0

Author Information
------------------

This role was created in 2020 by [Heath Taylor](https://twitter.com/datahattrick)
