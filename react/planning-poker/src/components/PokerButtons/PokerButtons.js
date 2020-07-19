import React, { Component } from 'react';
import PokerButton from '../PokerButton/PokerButton';


class PokerButtons extends Component {

    state = {
        scores: [1, 2, 3, 5, 8, 21, 40]
    }

    scoreSubmitted = (score) => {
        console.log("you clicked", score);
    }

    render() {
        const buttons = this.state.scores.map(
            (score, index) => <PokerButton
                key={index}
                score={score}
                onClick={() => this.scoreSubmitted(score)} />
        );

        return <div>{buttons}</div>;
    }

}

export default PokerButtons;
