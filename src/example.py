from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha512_crypt"])


hash = pwd_context.hash("1234")

hash_tmmp = "$6$rounds=656000$irG524JvndeE.qHu$E265dvT.MG/KD56jAb20i8HwSGTD2YJ/CewZ7N0SGwwnvxc494SY3XwDPGSyARrm2Yz.IfzHiOQRAWStoFtwL0"
res = pwd_context.verify("1234aaa", hash_tmmp)

print(res)
# print(hash)