indis - Icinga native director import service
----------------------------------------------

> This project is currently in alpha

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
output from Indis follow the Icinga2 objects structure and naming. This means that all Director configuration, like 
import rules, sync rules, apply rules etc, just need to operate on the "native" icinga2 object model. 
Instead of writing different rules and configuration depending on the structure of the source, Indis manage that 
separation and abstraction.

**That's why we call it "Icinga native director import service".**

# Use Icinga2 Director DSL

One key aspect with Icinga2 Director is to use the Director DSL to provide logic on howto connect objects together.
Typical the DSL can be used to connect services to hosts. Instead of create unique services for a host, use service 
templates and apply these based on host attributes like variables, hostgroups etc.

# Get started

For more hands on and get started check out the `config.yml` and the `demo` provider.

    python -m indis -f config.yml -s demo_source


# Output plugins 

Two output plugins are available, a json file plugin and a Icinga2 director API plugin.

## The json file output plugin

The json file output plugin can be used with fileshipper.

Check out the config:
```yaml
output:
  writer: indis.output.json_writer.JsonFileWriter
  configuration:
    directory: /tmp/director
```
The output will be written to the `directory`, with one file for each object typ.

## The Icinga2 director API output plugin

The output plugin will create and update objects using the Icinga2 director REST API.

> There is currently no support for DELETE and since the Director API is not managed by Import and Sync there is 
> now way from Icinga2 Director to manage the life cycle.
> The way this might be done is a pre-step, reading hosts from Icinga2 REST API to list existing hosts based on som 
> marker like hostgroup or host variable. The other options is to keep some cache from previous executions.

Configuration for the output plugin is:
```yaml
output:
  
  writer: indis.output.api_writer.APIWriter
  configuration:
    url: http://localhost/icingaweb2/director
    user: user
    password: password
```
The user must be an existing icinga2 web user with credentials for Director API.



# Source provider

TODO

> If you know Mender, you will recognize the programming structure of Indis providers.