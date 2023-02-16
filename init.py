from utils import func_Base, cryptoBase, parameters
import random
import json
SEED = 123
NAME = "user"
J = parameters.J
def init():
    p = cryptoBase.hash_to_prime(SEED,parameters.LAMBDA/2)[0]
    q = cryptoBase.hash_to_prime(SEED+SEED,parameters.LAMBDA/2)[0]
    N = p*q
    fai_N = (p-1)*(q-1)
    g = cryptoBase.generate_squre_root(N)
    e = cryptoBase.hash_to_prime(SEED,parameters.LAMBDA+parameters.LAMBDA1+parameters.LAMBDA2+2)[0]
    d = cryptoBase.generate_mutual_prime(e,fai_N)
    cnt = 0
    gd = pow(g, d, N)
    T_jian = []
    R = []
    daita_jian = 1
    h = []
    v = []
    v_value = 1
    for i in range(0, J):
        # T_jian.append(1)
        # k = random.randint(0, 1024)
        k = 1
        R.append(pow(g, k, N))
        T_jian.append(R[i])
        W = json.dumps([NAME, i, T_jian[i]])
        hi = func_Base.h(W)
        h.append(hi)
        u = func_Base.HPrime(json.dumps([NAME, i]))
        v.append(u)
        v_value *= u
        u_re = cryptoBase.generate_mutual_prime(u, (p-1)*(q-1))
        # u_re = 1
        # self.d = 1
        daita = pow(g, (hi+T_jian[i])*u_re*d, N)
        # re = cryptoBase.generate_mutual_prime((hi+msg)*self.d, self.N)
        daita_jian *= daita
        # self.W_list.append(W)
        # self.h_list.append(hi)
        # self.u_list.append(u)
        # self.sigma_list.append(sigma)

    u = 1
    # sk = (p,q,d,g,cnt,u)
    sk = {"p":p,"q":q,"d":d,"g":g,"cnt":cnt,"u":u, "NAME":NAME,"T_jian":T_jian,"e":e, "R":R, "daita_jian":daita_jian, "h":h, "v":v_value}
    pk = {"N":N,"g":g,"e":e,"gd":gd,"NAME":NAME,"T_jian":T_jian, "R":R, "daita_jian":daita_jian, "h":h, "v":v}
    sc = {"N":N,"g":g,"e":e,"gd":gd,"NAME":NAME, "daita_jian":daita_jian, "T_jian":T_jian}
    # pk = (N,g,e,gd,NAME,sigma_jian)
    return (sk,pk)



def main():
    (sk,pk) = init()
    print(sk)
    print(pk)
if __name__ == '__main__':
    main()