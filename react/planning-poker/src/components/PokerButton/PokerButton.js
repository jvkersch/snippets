import React from 'react';

const pokerButton = (props) => {
    return <button onClick={props.onClick}>
        {props.score}
    </button>
}

export default pokerButton;
