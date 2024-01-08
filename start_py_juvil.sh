eval `modulecmd bash purge`

export PYTHONPATH=/home/ssilburn/Python/lib:/home/cxs/jetspec:/home/ssilburn/Python/PSICIC/source/python:/home/cxs/datacube:/home/cxs/jetspec:/home/ssilburn/Python/juvil_dev/extras

eval `modulecmd bash load standard/2014-08-12`
eval `modulecmd bash load python/3.9`
eval `modulecmd bash load jet`
eval `modulecmd bash load mdsplus/6.1`
eval `modulecmd bash load idl`
eval `modulecmd bash load ipx`
eval `modulecmd bash load pgi`
#eval `modulecmd bash load pycharm-community/2022.1`

#add to path the public, latest JUVIL tools
export PYTHONPATH=$PYTHONPATH:~VSA/juvil-release/juvil/extras/
export PYTHONPATH=$PYTHONPATH:~VSA/juvil-release/juvil
