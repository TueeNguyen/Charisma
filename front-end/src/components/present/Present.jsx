import React from 'react';
import LetterCard from './lettercard/LetterCard'
import { CircularProgress } from '@mui/material';

export default function Present({displayBools, web3Data, address, message, wpi, mint}) {
  return (
    <section className="present">


        <div className="data-wrapper">
          <h1 className={!displayBools.clicked ? 'hidden' : ''}>{message}</h1>
          <div className="loading-circle">
            {displayBools.loading ? 
              <CircularProgress className='loading'/> 
            : 
            <div className="data">
              {wpi.split("").map((e, index) => {
                return (
                  <LetterCard hidden={web3Data.hidden} letter={e} index={index}/>
                )
              })}
            </div>}
          </div>
          
        </div>


        <div className="button-wrapper">
          {!displayBools.loading && web3Data.metaMaskAddress.toLowerCase() === address.toLowerCase() ? 
            <button 
              className={displayBools.hidden ? "mint hidden" : web3Data.minted ? 'mint blocked' : 'mint '} 
              disabled={web3Data.minted} 
              onClick={mint}>Mint as NFT
            </button> 
          : null}
        </div>
        
    </section>

  );
}
