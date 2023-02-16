import init
import utils.parameters as parameter
import json
import utils.func_Base as func_Base
import utils.cryptoBase as cryptoBase
import data_append
FILE = parameter.file_url
DATA_SIZA = parameter.DATA_SIZA
j = parameter.j
J = parameter.J

class User(data_append.User):
    def __init__(self, sk) -> None:
        super().__init__(sk,j)
    def data_query(self, msg, Fs, omega, i, T, R):
        print("T")
        print(T%self.N)
        msg1 = self.sigma_jian[j]
        vs = func_Base.HPrime(json.dumps([self.name, j]))
        u_re = cryptoBase.generate_mutual_prime(vs, (self.p-1)*(self.q-1))
        us_bar = self.v*u_re %((self.p-1)*(self.q-1))
        x = pow(self.daita_jian , us_bar, self.N)
        Fs_re = cryptoBase.generate_mutual_prime(omega, self.N)
        x = x*Fs_re %self.N
        y = pow(self.g, (self.h[j]+T)*self.d, self.N)
        sigma_s1 = func_Base.Shamir(x,y,vs,us_bar,self.N,(self.p-1)*(self.q-1))
        # print(s)
        tag1 = pow(sigma_s1, self.e*vs, self.N)
        tag2 = pow(self.g, self.h[j]+T, self.N)
        # return tag1 == tag2
        # print(self.sigma_list[i])
        # print(T)
        # print(tag1 == tag2)

        msg = cryptoBase.str_to_int(msg)
        us = func_Base.HPrime(json.dumps([self.name, i, j]))
        u_re = cryptoBase.generate_mutual_prime(us, (self.p-1)*(self.q-1))
        us_bar = self.u*u_re %((self.p-1)*(self.q-1))
        Rj = cryptoBase.generate_mutual_prime(R, self.N)
        x = pow(T*Rj, us_bar, self.N)
        Fs_re = cryptoBase.generate_mutual_prime(Fs, self.N)
        x = x*Fs_re %self.N
        y = pow(self.g, (self.h_list[i]+msg)*self.d, self.N)
        # print("y")
        # print(y)
        sigma_s = func_Base.Shamir(x,y,us,us_bar,self.N,(self.p-1)*(self.q-1))
        print("sigma_s")
        print(sigma_s%self.N)
        tag1 = pow(sigma_s, self.e*self.u_list[i], self.N)
        tag2 = pow(self.g, self.h_list[i]+msg, self.N)
        print(tag1 ==tag2)
        reply_msg = {"s":i, "j":j, "m":msg, "us":us, "sigma":sigma_s, "sigma_jian":T*Rj, "T":T, "R":R, "v":vs}
        return (tag1 ==tag2, reply_msg)


    


class Server(data_append.Server):
    def __init__(self, pk) -> None:
        super().__init__(pk, j)
    def data_query(self, i):
        print(self.sigma_list)
        value1 = 0
        for count in range(0, len(self.data)):
            if count != i:
                msg = cryptoBase.str_to_int(self.data[count])
                tem_value = self.h_list[count]+msg
                for count2 in range(0, len(self.u_list)):
                    if count2 != count and count2 != i:
                        tem_value *= self.u_list[count2]
                value1 += tem_value
        value1 = pow(self.gd, value1, self.N)
        # print(self.v)
        value2 = 0
        for count in range(0, J):
            if count != j:
                msg = self.sigma_jian[count]
                tem_value = self.h[count]+msg
                for count2 in range(0, len(self.v)):
                    if count2 != count and count2 != j:
                        tem_value *= self.v[count2]
                value2 += tem_value
        value2 = pow(self.gd, value2, self.N)
        # print(self.sigma_list)
        return (self.data[i], value1, value2, self.sigma_jian[j], self.R)

        


def main():
    (sk,pk) = init.init()
    user = User(sk)
    server = Server(pk)
    with open(FILE, "r") as f:
        m = f.read()
    (m_list, sigma_list) = user.append(m)
    server.append(m_list, sigma_list)
    i = 0
    (data, Fs, omega, T, R) = server.data_query(i)
    ans = user.data_query(data, Fs, omega,i, T, R)
    print(ans[0])
    


if __name__ == '__main__':
    main()