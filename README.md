# Example of a service using Butler client/server

This is an example of accessing Butler data using a web service.  This was
presented during the "Butler client-server" talk at the [SQRE services
bootcamp](https://confluence.lsstcorp.org/display/DM/SQuaRE+Bootcamp+-+May+6-10+2024).

Most of the meat is in the `get_coadd_url()` FastAPI handler in
`src/butlerexampleservice/handlers/external.py` -- the rest of this is just a
[Safir](https://safir.lsst.io) template project.

An example for a Phalanx deployment of this service can be found [here](https://github.com/lsst-sqre/phalanx/pull/3303).
