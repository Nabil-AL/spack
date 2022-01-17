from spack.pkg.builtin.launchmon import Launchmon as BuiltinLaunchmon


class Launchmon(BuiltinLaunchmon):
    def setup_build_environment(self, env):
        super().setup_build_environment(env)
        if self.spec.satisfies('%gcc@11:'):
            env.set('CXXFLAGS', '--std=c++14')