
import './App.css';
// import Web3 from 'web3';
import React, { useState } from 'react'




//const web3 = new Web3(new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/c5cd7d6606b14d1b890801407356df7b:8545'))


function App() {
  const truncateAccount = (addressList) => {
    let str = addressList.split("")
    let ret = "";
    for(var i = 0; i < 6; i++){
      ret += str[i]
    }
    ret += "..."
    for(i = addressList.length - 1; i > addressList.length - 5; i--){
      console.log('str[i]')
      ret += str[i]
    }
    console.log('ret is: ' + ret)
    return ret
  }

  let [user, setUser] = useState('Connect your wallet...');

  if(!window.ethereum){
    alert('No ethereum client detected, try MetaMask!')
  }else {
    window.ethereum.request({ method: 'eth_requestAccounts' }).then((addressList) => {
      setUser(truncateAccount(addressList[0]))
    })
  }

  return (
    <div className="App">
      <header className='header'>
        <h1>W<span id="blue">R</span></h1>
        <p>{user}</p>
      </header>
      
      <section className="hero">
        <h1>Wallet Rep</h1>
        <p>How do <i>you</i> translate into the metaverse?</p>
      </section>
      

      <section className="search">
        <input type="text" placeholder="Wallet address here..."/>
        <button>Analyze</button>
      </section>
      
      <section className="dataView">
        <p className="data">
          Insights will show up here...
        </p>
      </section>

    </div>
  );
}

export default App;
