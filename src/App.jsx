
import './App.css';
// import Web3 from 'web3';
import React, { useState, useEffect } from 'react'




//const web3 = new Web3(new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/c5cd7d6606b14d1b890801407356df7b:8545'))

// [NAME] is a tool that analyzes your personality through your NFT holdings and onchain activity.

// Introducing the Wallet Personality Indicator, the “WPI.”  Similar to the Myers-Briggs personality test, the WPI describes the personality attributes of a wallet, and therefore the personality of the wallet owner.

// We have identified the following wallet personality traits:
// D/P - Diamond Hands Connoisseur 💎or Paper Hands Trader Money Bags 🏦 
// O/U - Outperforming Index 📈 or Underperforming Index 📉 
// E/C - Early OG 🌅 / Crowd Follower 🦶🏽
// I/B - Indie Project Supporter 🆕  or Bluechip Projects Only   🔵

// What does your wallet say about you? 

// Want to meet others with similar personalities?  Want to learn from others who have different traits?  Mint a token here to connect to our Discord.


// How do you compare in the Metaverse?


function App() {

  let [user, setUser] = useState('Connect your wallet...')
  let [wpi, setWpi] = useState('')
  let [clicked, setClicked] = useState(false)
  let [hidden, setHidden] = useState(true)

  const truncateAccount = (addressList) => {
    let str = addressList.split("")
    let ret = "";
    for(var i = 0; i < 6; i++){
      ret += str[i]
    }
    ret += "..."
    for(i = addressList.length - 1; i > addressList.length - 5; i--){
      //console.log('str[i]')
      ret += str[i]
    }
    //console.log('ret is: ' + ret)
    return ret
  }

  const connectMetaMask = () => {
    if(!window.ethereum){
      alert('No ethereum client detected, try MetaMask!')
    }else {
      window.ethereum.request({ method: 'eth_requestAccounts' }).then((addressList) => {
        setUser(truncateAccount(addressList[0]))
      })
    }
  }
  
  const handleClick = () => {
      setWpi('DOEI')
      setClicked(true)
      setTimeout(() => {
        console.log('unhiding cards', hidden)
        setHidden(false)
        
      }, 1000)
      
  }

  useEffect(connectMetaMask, [])
  
  
  return (
    <div className="App">
      <header className='header'>
        <h1>C<span id="blue">h</span></h1>
        <p onClick={()=> connectMetaMask()}>{user}</p>
      </header>
      
      <section className="hero">
        <h1>Charisma</h1>
        <p>How do <i>you </i> translate into the metaverse?</p>
      </section>
      

      <section className="search">
        <input type="text" placeholder="Wallet address here..."/>
        <button onClick={handleClick}>{clicked ? 'Analyzing...' : 'Analyze'}</button>
      </section>
      
      <section className="dataView">
        <div className="data">
          {/* Insights will show up here... */}
          {wpi.split("").map((e, index) => {
            return (
              <div className={hidden ? 'letterCard hidden' : 'letterCard'} key={index}>
                <div className="letter " >
                  <div className='attribute'>{e}</div>
                  <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos fuga, consectetur natus aperiam nesciunt inventore.</p>
                </div>
              </div>
            )
          })}
        </div>
      </section>

    </div>
  );
}

export default App;
