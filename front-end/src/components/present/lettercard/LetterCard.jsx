import React from 'react';

export default function LetterCard({hidden, letter, index }) {
  return (
    <div className={hidden ? 'letterCard hidden' : 'letterCard'} key={index}>
        <div className="letter" >
            <div className='attribute'>{letter}</div>
        </div>
    </div>

  );
}
