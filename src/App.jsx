
import './App.css';

function App() {
  return (
    <div className="App">

      <h1>Wallet Rep</h1>
      <p>How do <i>you</i> translate into the metaverse?</p>

      <section className="search">
        <input type="text" placeholder="Wallet address here..."/>
        <button>Analyze</button>
      </section>
      
      <section className="dataView">
        <p className="data">
          Insights will show here...
        </p>
      </section>

    </div>
  );
}

export default App;
