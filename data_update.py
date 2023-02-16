import init
import utils.parameters as parameter
import json
import utils.func_Base as func_Base
import utils.cryptoBase as cryptoBase
import data_query
FILE = parameter.file_url
DATA_SIZA = parameter.DATA_SIZA
J = parameter.J

class User(data_query.User):
    def __init__(self, sk) -> None:
        super().__init__(sk)
    def data_query(self, msg, Fs, omega, i, T, R):
        ans = super().data_query(msg, Fs, omega, i, T, R)
        msg = cryptoBase.str_to_int(msg)
        self.reply_msg = ans[1]
        # self.hs = self.h_list[i]
        return ans

    def data_update(self, m_new):
        para = self.reply_msg
        msg_new = cryptoBase.str_to_int(m_new)
        W = json.dumps([self.name, para["s"],  para["j"],func_Base.h(msg_new)])
        hs = func_Base.h(W)
        u_re = cryptoBase.generate_mutual_prime(para["us"], (self.p-1)*(self.q-1))
        sigma_s = pow(self.g, (hs+msg_new)*u_re*self.d, self.N)


        sigma_re = cryptoBase.generate_mutual_prime(para["sigma"], self.N)
        self.sigma_jian = para["sigma_jian"]*sigma_re*sigma_s%self.N
        # self.sigma_jian = para["sigma_jian"]

        hj = self.h[para["j"]]
        v_re = cryptoBase.generate_mutual_prime(para["v"], (self.p-1)*(self.q-1))
        self.T = self.sigma_jian*para["R"]
        print("new T:")
        print(self.T%self.N)
        print(para["v"])
        sigma = pow(self.g, (hj+self.T%self.N)*v_re*self.d, self.N)
        sigma_jian_re = cryptoBase.generate_mutual_prime(para["sigma_jian"], self.N)
        self.daita_jian = self.daita_jian*sigma_jian_re*sigma%self.N
        # print(self.sigma_jian)
        return (para["s"], para["j"], m_new, sigma_s,sigma, (self.p-1)*(self.q-1))


    


class Server(data_query.Server):
    def __init__(self, pk) -> None:
        super().__init__(pk)
    def data_update(self, quest):
        (s, j, m_new, sigma_s, daita_jian, fai_N) = quest
        msg_new = cryptoBase.str_to_int(m_new)
        W = json.dumps([self.name, s, j,func_Base.h(msg_new)])
        hs = func_Base.h(W)
        tag1 = pow(sigma_s, self.e*self.u_list[s], self.N)
        tag2 = pow(self.g, hs+msg_new, self.N)
        # tag1 = pow(sigma_list[i], self.e*ui, self.N)
        # tag2 = pow(self.g, hi+msg, self.N))
        print(tag1 ==tag2)
        if tag1 != tag2:
            return "error"
        sigma_re = cryptoBase.generate_mutual_prime(self.sigma_list[s], self.N)

        self.sigma_list[s] = sigma_s
        self.sigma_jian[j] = self.sigma_jian[j]*sigma_re*sigma_s%self.N
        # print(tem%self.N)
        # print( self.sigma_jian[j])
        # if tag1 == tag2:
        #     self.data[s] = m_new
        #     sigma_re = cryptoBase.generate_mutual_prime(self.sigma_list[s], self.N)
        #     self.sigma_jian = self.sigma_jian*sigma_re*sigma_s%self.N  
        #     self.sigma_list[s] = sigma_s
        # print(self.sigma_jian)

        R = self.R
        # print(self.sigma_jian)
        # print("new T:")
        self.T = self.sigma_jian[j]
        # print(self.T%fai_N)
        hj = self.h[j]
        # print(self.v[j])
        # print(self.sigma_jian)
        # sigma = pow(self.g, (hj+self.T)*v_re*self.d, self.N)
        # print(self.v)
        tag1 = pow(daita_jian, self.e*self.v[j], self.N)
        tag2 = pow(self.g, hj+self.T, self.N)
        print(tag1)
        print(tag2)
        print(tag1 ==tag2)
        return tag1 ==tag2


        


def main():
    (sk,pk) = init.init()
    user = User(sk)
    server = Server(pk)
    with open(FILE, "r") as f:
        m = f.read()
    (m_list, sigma_list) = user.append(m)
    server.append(m_list, sigma_list)
    i = 5
    (data, Fs, omega, T, R) = server.data_query(i)
    ans = user.data_query(data, Fs, omega,i, T, R)
    quest = user.data_update("aaaaaaaaaaaaaaaaaaaa")
    server.data_update(quest)
    # print(ans)
    


if __name__ == '__main__':
    main()