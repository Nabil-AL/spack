from spack.pkg.builtin.libzmq import Libzmq as BuiltinLibzmq


class Libzmq(BuiltinLibzmq):
    __doc__ = BuiltinLibzmq.__doc__

    def configure_args(self):
        config_args = super().configure_args()
        if "+libsodium" not in self.spec:
            config_args.append("--without-libsodium")
        return config_args
