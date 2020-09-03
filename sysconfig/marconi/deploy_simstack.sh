#!/bin/bash
set -x
set -e

# Deployment directory
BASE_DIR=/m100/home/userexternal/jblancoa/hbp-spack-deployments
#DEPLOYMENT_HOME=$BASE_DIR/softwares/$(date '+%d-%m-%Y')
DEPLOYMENT_HOME=$BASE_DIR/softwares/27-08-2020

mkdir -p $DEPLOYMENT_HOME
mkdir -p $DEPLOYMENT_HOME/sources
mkdir -p $DEPLOYMENT_HOME/install

export HOME=$DEPLOYMENT_HOME

# Clone spack repository
cd $DEPLOYMENT_HOME/sources
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git -b marconi_deployment

# Setup environment
export SPACK_ROOT=`pwd`/spack
export PATH=$SPACK_ROOT/bin:$PATH
source $SPACK_ROOT/share/spack/setup-env.sh

#chmod -R ugo+w $DEPLOYMENT_HOME
# Copy configurations
mkdir -p $SPACK_ROOT/etc/spack/defaults/linux/
cp $SPACK_ROOT/sysconfig/marconi/* $SPACK_ROOT/etc/spack/defaults/linux/

# Directory for deployment
export SPACK_INSTALL_PREFIX=$DEPLOYMENT_HOME/install

spack reindex
module load profile/advanced
module load gnu/8.4.0 cuda/10.1
module load spectrum_mpi/10.3.1--binary boost/1.72.0--spectrum_mpi--10.3.1--binary
module load cmake/3.17.1

spack module tcl refresh -y --delete-tree
module list

export LD_LIBRARY_PATH=/cineca/prod/opt/compilers/python/3.7.8/none/lib:$LD_LIBRARY_PATH

export LC_CTYPE=en_US.UTF-8

# PYTHON 3 packages
spack spec -Il neurodamus-hippocampus+coreneuron ^python@3.7.8
spack install --dirty --keep-stage neurodamus-hippocampus+coreneuron ^python@3.7.8
spack install --dirty --keep-stage neurodamus-neocortex+coreneuron ^python@3.7.8
spack install --dirty --keep-stage neurodamus-mousify+coreneuron ^python@3.7.8

spack spec -Il py-neurodamus ^python@3.7.8
spack install --dirty py-neurodamus ^python@3.7.8

##spack spec -I neuron~mpi %intel ^python@3.6.5
##spack install --dirty --keep-stage -v neuron~mpi %intel ^python@3.6.5

#module swap PrgEnv-intel PrgEnv-gnu
spack spec -Il py-bluepy ^python@3.7.8
spack install --dirty --keep-stage -v py-bluepy ^python@3.7.8

#spack spec -Il py-sonata-network-reduction%gcc ^python@3.6.5 ^zeromq%intel@18.0.1.163 ^spdlog%gcc ^cmake@3.15.3
#spack install --dirty --keep-stage -v py-sonata-network-reduction%gcc ^python@3.6.5 ^zeromq%intel@18.0.1.163 ^spdlog%gcc ^cmake@3.15.3

spack spec -Il py-bluepyopt ^python@3.7.8
spack install --dirty --keep-stage py-bluepyopt ^python@3.7.8

#spack spec -Il psp-validation%gcc ^python@3.6.5 ^cmake@3.15.3 ^py-pandas@0.25.3 ^py-h5py@2.10.0
#spack install --dirty psp-validation%gcc ^python@3.6.5 ^cmake@3.15.3 ^py-pandas@0.25.3 ^py-h5py@2.10.0

# Re-generate modules
spack module tcl refresh --delete-tree -y
cd $DEPLOYMENT_HOME/install/modules/tcl/linux-rhel7-power9le
find py* -type f -print0|xargs -0 sed -i '/PYTHONPATH.*\/neuron-/d'
find neuro* -type f -print0|xargs -0 sed -i '/module load mpich/d'

#ln -s $DEPLOYMENT_HOME/install/modules/tcl/linux-rhel7-power9le $DEPLOYMENT_HOME/modules
#chmod -R ugo-w $DEPLOYMENT_HOME

#cd $BASE_DIR
#rm modules
#ln -s $DEPLOYMENT_HOME/install/modules/tcl/linux-rhel7-power9le modules
