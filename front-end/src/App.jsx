
import './App.css';
import Web3 from 'web3';
import React, { useState, useEffect } from 'react'
import CharismaNFT from './abi/CharismaNFT.json'
//Components
import Header from './components/header/Header'
import SearchBar from './components/searchbar/SearchBar'
import Present from './components/present/Present'

const axios = require('axios').default
// const web3 = new Web3(new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/c5cd7d6606b14d1b890801407356df7b:8545'))


function App() {
  let [wpi, setWpi] = useState('')
  let [message, setMessage] = useState('')
  //display Bools
  let [displayBools, setDisplayBools] = useState({clicked: false, hidden: true, showExplanation: false, loading: false})
  //Web3 Data
  let [web3Data, setWeb3Data] = useState({metaMaskAddress: '', stateContract: null, minted: false, address: ''})
  let [internalAddress, setInternalAddress] = useState('')

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

  const getData = (addr) => {
    console.log('polling api for address: ' + addr)
    //addr = '0x24daBabEE6BF5f221B64890E424609Ff43d6E148'
    axios({
      method: 'GET',
      url: 'https://charisma-api.azurewebsites.net/address/' + addr
    })
    .then((response) => {
      let wpi = ''
      for(const dimension in response.data.dimensions){
        wpi = wpi.concat(response.data.dimensions[dimension].value)
      }
      setWpi(wpi)
      setTimeout(() => {
        setDisplayBools(prevState => { return {...prevState, hidden: false, loading: false}})
      }, 500)
    })
    .catch((error) => {
      setTimeout(() => {
        setDisplayBools(prevState => { return {...prevState, hidden: false, loading: false}})
      }, 500)
      setWpi('ABCD')
    })
  }

  const loadBlockChainData = async () => {
    if(!window.ethereum){
      alert('No ethereum client detected, try MetaMask!')
    }
      

    const web3 = new Web3(Web3.givenProvider)
    let accounts = await window.ethereum.request({ method: 'eth_requestAccounts' })
    let user = accounts[0]
    
    setWeb3Data(prevState => { return {...prevState, metaMaskAddress: user ? user : ''}})
    // setMetaMaskAddress(user)

    const networkId = await web3.eth.net.getId()
    const networkData = CharismaNFT.networks[networkId]
    console.log(networkId)
    if(networkData) {
      console.log(networkData)
      const abi = CharismaNFT.abi
      console.log(abi)
      const contractAddress = networkData.address
      let contract = await new web3.eth.Contract(abi, contractAddress);
      if(contract){
        console.log(contract)
        setWeb3Data(prevState => { return {...prevState, stateContract: contract}})
        // setStateContract(contract)
      }
      else {
        alert('Smart Contract Not Deployed To Network')
      }
    }
  }

  const mint = async () => {
    if(web3Data.stateContract){
      await web3Data.stateContract.methods.mint(wpi).send({from: web3Data.metaMaskAddress})
      console.log('Minted!')
      setWeb3Data(prevState => { return {...prevState, minted: true}})
      
    }
  }

  const handleSearchChange = (event) => {
    setWeb3Data(prevState => { return {...prevState, address:event.target.value}})
  }
  
  const handleSearchClick = () => {
    //check for whitespace or empty string
    if(web3Data.address && web3Data.address.length > 0 && /\s/.test(web3Data.address) === false){
      setMessage('You are a...')
      setDisplayBools(prevState => {return {...prevState, clicked: true, hidden: true, loading: true}})
      getData(web3Data.address)
      setInternalAddress(web3Data.address)
    }
    else {
      setMessage('Please enter a valid ETH address')
      setDisplayBools(prevState => {return {...prevState, clicked: true}})
    }
  }

  const handleMoreInfoClick = () => {
    setDisplayBools(prevState =>  {return {showExplanation: !prevState.showExplanation}})
  }

  const handleMetaMaskClick = () => {
    if(!web3Data.metaMaskAddress)
      loadBlockChainData()
    else{
      navigator.clipboard.writeText(web3Data.metaMaskAddress);
      alert('Address Copied')
    }
      
  }

  useEffect(() => {
    async function loadbcd(){
      await loadBlockChainData()
    }

    loadbcd()
  }, [])

  useEffect(() => {
    
  }, [displayBools.loading])

  return (
    <div className="App">
      <Header handleMetaMaskClick={handleMetaMaskClick} user={web3Data.metaMaskAddress ? truncateAccount(web3Data.metaMaskAddress) : 'Connect Wallet'}/>
      
      <section className="hero">
        <h1>Charisma</h1>
        <p>What does your wallet say about <i>you</i>?</p>
      </section>

      <SearchBar 
        address={web3Data.address} 
        handleSearchChange={handleSearchChange} 
        handleSearchClick={handleSearchClick} 
        clicked={displayBools.clicked}
      />

      <Present 
        displayBools={displayBools}
        web3Data={web3Data} 
        address={internalAddress}
        message={message} 
        wpi={wpi} 
        mint={mint}
      />

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

      <section className={displayBools.showExplanation ? "explanation" : "explanation hidden"}>
        <div className="wrapper">
          
          <h1>How your results are Calculated</h1>

          <h2>D/P - Diamond Hands Connoisseur / Paper Hands Trader:</h2>
          <p>
            If the ratio of sell transactions (outgoing transfer) to the number of buy transactions (incoming transfer) is 30% or less, then the wallet will receive the “D” attribute (💎). <br />
            If it is greater than 30%, the wallet will receive the "P" attribute (🧻)
          </p>
          
          <h2>Outperforming Index / Underperforming Index:</h2>
          <p>
            We're comparing the performance of the current NFT portfolio with the performance of ETH over the same time period.  Time period begins at the purchase date of the earliest NFT currently in the wallet until now. <br />
            Performance of the current NFT portfolio is calculated as the difference between
          
            <br />  
            <span>(1) the sum of the purchase price of the NFTs currently in wallet and</span>
            <br />
            <span>(2) the sum of the 7-day average sale price for each NFT. </span>
          
          
            If the percentage performance of the current NFT portfolio is better than the percentage performance of ETH over the same time period, then the wallet will receive the “O” attribute (📈). <br />
            If the percentage performance of the current NFT portfolio is worse than the percentage performance of ETH over the same time period, then the wallet will receive the “U” attribute (📉). <br />
          </p>
          
          <h2>Early OG / Crowd Follower:</h2>
          <p>
            The purchase of an NFT within 1 week of the project launch date is an indication that you are an early supporter of that project.  <br />
            If the number of NFTs purchased within 1 week of project launch is 20% or more of the total number of NFTs that you have in the wallet, then the wallet will receive the “E” attribute (🌅). <br />
            If the number of NFTs purchased within 1 week of project launch is less than 20% of the total number of NFTs that you have in the wallet, then the wallet will receive the “C” attribute (🦶🏽).
          </p>
          
          <h2>Small Project Supporter / Bluechip Shark:</h2>
          <p>
            We use the total trade volume as a proxy for how established an NFT project is.
            “Small project” is defined as a project with a total trade volume of 2,000 ETH or less.  A “blue chip project” is defined as a project with a total trade volume of greater than 2,000 ETH. <br />
            If the ratio of the number of small project NFTs compared to the number of blue chip project NFTs is equal to or greater than 50%, then the wallet will receive the “S” attribute (🐣). <br />
            If the ratio of the number of small project NFTs compared to the number of blue chip project NFTs is less than 50%, then the wallet will receive the “B” attribute (🔵).

          </p>
          
          <button onClick={handleMoreInfoClick}>close</button>
        </div>
        
      </section>

      <footer className="footer">

        <p>{"Developed with <3 By Joyce, Lexi, Dave, Tue & Alex at NFTHack2022"}</p>

      </footer>
    </div>
  );
}

export default App;
