
import './App.css';
// const Web3 = require('web3')


// const web3 = new Web3(Web3.givenProvider) 
//const web3 = new Web3(new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/c5cd7d6606b14d1b890801407356df7b:8545'))



function App() {
  return (
    <div className="App">
      <header className='header'>
        <h1>W<span id="blue">R</span></h1>
        <p>Connect your wallet...</p>
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
