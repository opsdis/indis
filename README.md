indis - Icinga native director import service
----------------------------------------------

# Overview 

Indis is a configuration tool for Icinga2 and integrates with the Icinga2 module Director. 
With Indis it possible to read data from other system that provide data that can be used to create
Icinga2 objects, like hosts, services, hostgroups, dependency etc.
The source system is read by indis source providers. A provider mediate between the source native data model and 
data format to the native icinga2 objects. A provider is typical something that is customized for a specific source 
system, e.g. a network management system where all routers and switches is managed. 

After the provider has created the icinga objects, the data is processed by a number of configurable processors. 
A processor can typical be logic that enrich or transform the icinga objects in some way, e.g. adding host vars.

The final step is to generate the output, the output data that should be processed by Icinga2 Director.

The major benefit using Indis compared to other integrations like a custom json, a sql table etc, is that all
output from Indis follow the Icinga2 object naming. This means that all Director configuration, like import rules, 
sync rules, apply rules etc, just need to operate on the "native" icinga2 object model. Instead of writing different 
rules and configuration depending on the structure of the source, Indis manage that separation and abstraction. 
That's why we call it "Icinga native director import service".

For more hands on and get started check out the `config.yml` and the `demo` provider.

    python -m indis -f config.yml -s demo_source

# Output 
Currently, only a json output to file is provided. This can be used with fileshipper.

Check out the config:
```yaml
output:
  writer: indis.output.json_writer.JsonFileWriter
  configuration:
    directory: /tmp/director
```
The output will be written to the `directory`, with one file for each object typ. 
