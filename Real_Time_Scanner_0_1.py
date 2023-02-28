from requests.sessions import session
import asyncio
import aiohttp
import requests
import json
import time
import web3
from web3 import Web3
from web3.eth import AsyncEth


class BlockScanner:
    def __init__(self, block_number=-1):
        self.tokens = [] # ваши ethersan токены

        self.token = "UNZPFZH11HR8AX94HWS7HFGCPH95XQRECY" # это первыый токен из живых в списке
        self.block_number = block_number
        # номер используемого токена для данной транзакции
        self.number_of_token = 0
        # в этой переменной будут храниться все временнные значения транзакций
        self.list_of_transactions = list()
        self.ERC20_ABI = json.loads(
            '''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')
        # в этой переменной будут храниться значения {"адрес контракта" : (имя токена, разрядность)}
        self.contracts = {'0x0000000000000000000000000000000000000000': [18, 'eth', 'ethereum'], '0x3845badade8e6dff049820680d1f14bd3903a5d0': [18, 'SAND', 'SAND'], '0xdac17f958d2ee523a2206206994597c13d831ec7': [6, 'USDT', 'Tether USD'], '0x9506d37f70eb4c3d79c398d326c871abbf10521d': [18, 'MLT', 'Media Licensing Token'], '0x05237e2bd2dfab39a135d254cabae94b183c8bad': [8, 'BPTC', 'Business Platform Tomato Coin'], '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': [6, 'USDC', 'USD Coin'], '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2': [18, 'WETH', 'Wrapped Ether'], '0x3affcca64c2a6f4e3b6bd9c64cd2c969efd1ecbe': [18, 'DSLA', 'DSLA'], '0x205e982d0ba8814ecd76e2e296d92345968f1292': [18, 'KENNEL', 'Kennel'], '0x6c6ee5e31d828de241282b9606c8e98ea48526e2': [18, 'HOT', 'HoloToken'], '0x4a1d542b52a95ad01ddc70c2e7df0c7bbaadc56f': [18, 'NIFT', 'Niftify'], '0xfe656b735b328ae5394d7c1651803175844a5cfc': [9, 'AKIMITSU', 'Akimitsu'], '0xc944e90c64b2c07662a292be6244bdf05cda44a7': [18, 'GRT', 'Graph Token'], '0x32353a6c91143bfd6c7d363b546e62a9a2489a20': [18, 'AGLD', 'Adventure Gold'], '0x249e38ea4102d0cf8264d3701f1a0e39c4f2dc3b': [18, 'UFO', 'THE TRUTH'], '0xaea46a60368a7bd060eec7df8cba43b7ef41ad85': [18, 'FET', 'Fetch'], '0x8ab7404063ec4dbcfd4598215992dc3f8ec853d7': [18, 'AKRO', 'Akropolis'], '0x4d224452801aced8b2f0aebe155379bb5d594381': [18, 'APE', 'ApeCoin'], '0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0': [18, 'MATIC', 'Matic Token'], '0xc1a0d24a91cde075d4a5600e374589731fe42e97': [9, 'BASILISK', 'THE BASILISK'], '0x5a98fcbea516cf06857215779fd812ca3bef1b32': [18, 'LDO', 'Lido DAO Token'], '0x15d4c048f83bd7e37d49ea4c83a07267ec4203da': [8, 'GALA', 'Gala']}

        # объект для доступа к web3
        self.web3 , self.web3_not_async = self.connect_to_web3()

    def connect_to_web3(self):
        web3_con = Web3(Web3.AsyncHTTPProvider("https://eth.llamarpc.com"),
                        modules={'eth': (AsyncEth,)},
                        middlewares=[])
        web3_con1 = web3.Web3(web3.HTTPProvider("https://eth.llamarpc.com"))
        print(f'isConnected with WEB3 : {web3_con.isConnected()}')
        print(f"number of current chain is {web3_con.eth.chain_id}")
        return web3_con,web3_con1

    # вход - время , выход - целочисленное значение предыдущего созданного блока
    def get_block_number_by_timestamp(self, timestamp=round(time.time()), token=''):
        if token == '': token = self.token
        return int(json.loads(requests.get(
            f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={token}").content)[
                       'result'])
        return self.web3_not_async.eth.get

    # вход - целочисленное значение блока, выход - список хэшей транзакций в блоке
    def eth_getBlockByNumber(self, block_number=0, token=''):
        if token == '': token = self.token
        res = json.loads(requests.get(
            f'https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={hex(block_number)}&boolean=true&apikey={token}').content)[
            'result']['transactions']
        return [
            transaction['hash'] for transaction in res]

    # ввод список хэшей транзакций в блоке , выход - чтение всех хэшей
    async def read_transactions_hash(self, transactions):
        async with aiohttp.ClientSession() as session:
            print(f'number of transactions is {len(transactions)}')
            await asyncio.gather(*[self.make_request_to_etherscan(session, i) for i in transactions])

    def next_token(self):
        self.number_of_token += 1
        if self.number_of_token > (len(self.tokens)-1):
            self.number_of_token = 0
        return self.tokens[self.number_of_token]

    # вход - объект подключения, запрос, выход - заполнение кортежа self.tuple_of_transactions
    async def make_request_to_etherscan(self, session, txhash):
        # блок выбора токена: они чередуются потому что
        # для каждого токена ограничение 5 вызовов в секунду
        token = self.next_token()
        req = f'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={txhash}&apikey={token}'
        async with session.get(req) as resp:
            # тут может веррнуться строка "Max limit reached!" если токен используется больше 5 раз в секунду -> TypeError
            # может вернуться пустой список, если переводился ethereum -> IndexError
            # если переводился токен, вернется список 'logs'
            if resp.status == 200:
                res = json.loads(await resp.text())['result']
                if type(res)==str:
                    print('TOKEN USING TOO MUCH')
                elif res['logs']==[]:
                    async with session.get(f'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={txhash}&apikey={self.next_token()}') as eth_trans:
                        if eth_trans.status==200:
                            eth_tr = json.loads(await eth_trans.text())['result']
                            if type(eth_tr) != str:
                                self.list_of_transactions.append([int(eth_tr['value'],0),  res['from'], res['to'], '0x0000000000000000000000000000000000000000',18,'eth','ethereum'])
                elif res['logs'][0]['data']=='0x':
                    pass
                else:
                    self.list_of_transactions.append([int(res['logs'][0]['data'], 0), res['from'], res['to'],res['logs'][0]['address']])


                # (value - from - to - contract_address) -> self.list_of_transactions

    # эта функция будет вызываться только тогда, когда в словаре self.contracts,
    # когда нет ключа с адресом данного контракта, в других случаях мы не будем вызывать эту функцию
    # на вход подается список [value, from , to, address]
    # в конце в случае вызова этой функции в self.contracts дописываются значения полученные
    # в этой функции для меньшего количества вызовов к ней
    def get_token_symbol(self, list_of_transaction):
        addr = self.web3.toChecksumAddress(list_of_transaction[3])
        tokenContract =  self.web3_not_async.eth.contract(addr, abi= self.ERC20_ABI)
        #print('tokenContract: ',tokenContract, 'type: ', type(tokenContract))
        #decimal = await tokenContract.functions.decimals().call()
        #tokenName = await tokenContract.functions.symbol().call()
        #tokenFullName = await tokenContract.functions.name().call()
        try:
            res = [tokenContract.functions.decimals().call(), tokenContract.functions.symbol().call(),  tokenContract.functions.name().call()]
            #print('res: ', res)
            # добавляем в словарь список [decimal, tokenName, tokenFullName]
            self.contracts[list_of_transaction[3]] = res
            list_of_transaction += res
        except:
            pass
            #print('lose')

    # эта функция проверяет есть ли адрес контракта в self.contracts
    # если есть, то запроса не происходит, и значения из словаря self.contracts
    # просто дописываются, а если в self.contracts нет адреса контракта,
    # то вызывается функция self.get_token_symbol()
    def update_list_of_transactions(self):
        [self.get_token_symbol(list_of_transaction)
                                   if (list_of_transaction[3] not in self.contracts)
                                   else list_of_transaction + self.contracts[list_of_transaction[3]]
                                   for list_of_transaction in self.list_of_transactions]

    # эта функция дописывает в self.list_of_transactions стоимость переведенных активов
    # вызывается когда в self.list_of_transactions хранятсся транзакции в виде:
    # [ value , from , to , contract_address , decimal, tokenName, tokenFullName]
    # если не удалось определить цену функция вернет -1
    async def update_list_of_transactions_for_price(self):
        pass

    async def main(self):
        transactions = self.eth_getBlockByNumber(
            self.get_block_number_by_timestamp() if self.block_number == -1 else self.block_number)
        # выше мы получили список хэшей транзакций в блоке
        await self.read_transactions_hash(transactions)
        #print(self.list_of_transactions)
        # выше мы получаем в переменной self.list_of_transaction список информации
        # о каждой транзакции в виде (value - from - to - contract_address)

        self.update_list_of_transactions()
        # выше мы получаем для каждой транзакции значения (decimal, tokenName, tokenFullName)
        # и дописываем их в соответствующую запись в списке self.list_of_transactions
        # получаем вид = [ value , from , to , contract_address , decimal, tokenName, tokenFullName]


scan = BlockScanner()
start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(scan.main())

finish = time.time()
print(f'время выполнения : {finish - start}')
for i in scan.list_of_transactions:
    print(i)
print(f'Обработано транзакций : {len(scan.list_of_transactions)}')
print(scan.contracts)