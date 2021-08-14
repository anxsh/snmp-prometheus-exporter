# snmp-prometheus-exporter

# Dependencies

```
sudo apt-get install snmp snmpd python-netsnmp python-yaml
```

# Installation

Create a config file (based on config_sample.yaml) and put it at `/etc/snmp-prometheus-exporter.yml`

```
sudo cp snmp-prometheus-exporter.py /usr/local/bin
sudo cp snmp-prometheus-exporter.service /etc/systemd/system/
sudo systemctl start snmp-prometheus-exporter.service
sudo systemctl enable snmp-prometheus-exporter.service
```
