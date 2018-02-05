LittleMuscle
============

LittleMuscle aims to be the simplest possible complete implementation of the
theory of multiscale computing developed by [Borgdorff. et al
(2013)](https://doi.org/10.1016/j.jpdc.2012.12.011). It runs a set of submodels
in a single Python instance with a single thread.

While LittleMuscle fulfils a similar role to MUSCLE, in that it ties submodels
together, and the API for implementing submodels is similar to that of
MUSCLE-HPC and the future MUSCLE 3, the execution engine in LittleMuscle is very
different, and by its nature, LittleMuscle does not scale at all. It is intended
for rapid prototyping and for learning the theory.

LittleMuscle is in early development, so feel free to play with it, but don't
use it for anything important, because it will change rapidly and break your
stuff.


Legal
=====

Copyright 2018 University of Amsterdam and Netherlands eScience Center

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
