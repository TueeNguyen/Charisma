
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
  let [showExplanation, setShowExplanation] = useState(false)

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
      setWpi('DOES')
      setClicked(true)
      setTimeout(() => {
        console.log('unhiding cards', hidden)
        setHidden(false)
        
      }, 1000)
  }

  const handleMoreInfoClick = () => {
    setShowExplanation(!showExplanation)
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
        <p>What does your wallet say about <i>you</i>?</p>
      </section>

      <section className="search">
        <input type="text" placeholder="Wallet address here..."/>
        <button onClick={handleClick}>{clicked ? 'Analyzed!' : 'Analyze'}</button>
      </section>

      <section className="present">
        <h1 className={!clicked ? 'hidden' : ''}>You are a... </h1>
        <div className="data">
          {/* Insights will show up here... */}
          {wpi.split("").map((e, index) => {
            return (
              <div className={hidden ? 'letterCard hidden' : 'letterCard'} key={index}>
                <div className="letter" >
                  <div className='attribute'>{e}</div>
                  {/* <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos fuga, consectetur natus aperiam nesciunt inventore.</p> */}
                </div>
              </div>
            )
          })}
        </div>
      </section>

      <section className="legend">
        <h1>What your result means:</h1>
        <p>
        <span className="big">D/P</span> - Diamond Hands Connoisseur 💎| Paper Hands Trader Money Bags 🏦
        <br />
        {/* If (number of out transactions / number of in transactions) is less than 30%, then Diamond Hands. */}
        <span className="big">O/U</span> - Outperforming Index 📈 | Underperforming Index 📉
        <br />
        {/* (Sum of the 7 day average sale price of the NFTs currently in the wallet) - (Sum of the purchase price of the NFTs currently in wallet.) / Sum of the purchase price of the NFTs currently in wallet. → compare it with the change in ETH price over the same time period. */}
        <span className="big">E/C</span> - Early OG 🌅 | Crowd Follower 🦶🏽
        <br />
        {/* Purchase within 1 week of launch 
        Number of NFTs purchased within 1 week of launch / total number of NFTs.  If > 20%, then Early OG. */}
        <span className="big">S/B</span> - Small Project Supporter | Bluechip Project Shark   🔵
        
        {/* Assumption - The greater than trade volume, the more established the project.
        Do you own any indie NFTs right now? 
        Threshold - 2000 Eth all time trade volume
        Number of small project NFTs / total number of NFTs.  If greater than 50%, then Small Project Support */}
        </p>

        <button className='info' onClick={handleMoreInfoClick} href=".explanation">How are these values determined?</button>
      </section>

      <footer className="footer">

        <p>{"Developed with <3 By Joyce, Lexi, Dave, Tue & Alex at NFTHack2022"}</p>

      </footer>

      <section className={showExplanation ? "explanation" : "explanation hidden"}>
        <div className="wrapper">
          
          <h1>How your results are Calculated</h1>
          <h2>Diamond Hands / Paper Hands:</h2>
          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis, ut sunt. Doloremque exercitationem magni temporibus.</p>
          <h2>Outperforming Index / Underperforming Index:</h2>
          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis, ut sunt. Doloremque exercitationem magni temporibus.</p>
          <h2>Early OG / Crowd Follower:</h2>
          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis, ut sunt. Doloremque exercitationem magni temporibus.</p>
          <h2>Small Project Supporter / Bluechip Shark:</h2>
          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis, ut sunt. Doloremque exercitationem magni temporibus.</p>
          <button onClick={handleMoreInfoClick}>close</button>
        </div>
        
      </section>
    </div>
  );
}

export default App;
