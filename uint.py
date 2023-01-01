from base.wrapper import Wrapper


@Wrapper.wrap(bits=8)
class BYTE(Wrapper):
    @property
    def u16(self):
        return WORD.new(self)

    @property
    def u32(self):
        return DWORD.new(self)

    @property
    def u64(self):
        return QWORD.new(self)

    @property
    def u128(self):
        return OWORD.new(self)


@Wrapper.wrap(bits=16)
class WORD(Wrapper):
    @property
    def u8(self):
        return BYTE.new(self)

    @property
    def u32(self):
        return DWORD.new(self)

    @property
    def u64(self):
        return QWORD.new(self)

    @property
    def u128(self):
        return OWORD.new(self)


@Wrapper.wrap(bits=32)
class DWORD(Wrapper):
    @property
    def u8(self):
        return BYTE.new(self)

    @property
    def u16(self):
        return WORD.new(self)

    @property
    def u64(self):
        return QWORD.new(self)

    @property
    def u128(self):
        return OWORD.new(self)


@Wrapper.wrap(bits=64)
class QWORD(Wrapper):
    @property
    def u8(self):
        return BYTE.new(self)

    @property
    def u16(self):
        return WORD.new(self)

    @property
    def u32(self):
        return DWORD.new(self)

    @property
    def u128(self):
        return OWORD.new(self)


@Wrapper.wrap(bits=128)
class OWORD(Wrapper):
    @property
    def u8(self):
        return BYTE.new(self)

    @property
    def u16(self):
        return WORD.new(self)

    @property
    def u32(self):
        return DWORD.new(self)

    @property
    def u64(self):
        return QWORD.new(self)
