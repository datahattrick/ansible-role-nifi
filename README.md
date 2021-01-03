Role Name
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


Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
