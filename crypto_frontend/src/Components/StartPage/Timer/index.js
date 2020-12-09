import React from 'react';
import './style.css'
import Alert from "reactstrap/es/Alert";

export default class ExpTimer extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            expiration_date: 1558344909061,
            milisecsRemaining: 0,
            isOver: false,
            time: {}
        };
        this.countDown = this.countDown.bind(this)

    }

    startTimer() {
        setInterval(this.countDown, 500);
    }

    countDown() {
        let milisecsRemaining = this.state.milisecsRemaining - 500;
        this.setState({
            milisecsRemaining: milisecsRemaining,
        });

        if (milisecsRemaining < 900) {
            this.setState({isOver: true})

        }
    }

    renderRemainingTime(milis) {
        let hours = ("0" + parseInt(milis / (60 * 1000 * 60))).slice(-2);
        let mins = ("0" + parseInt((milis - hours * 60 * 1000 * 60) / (60 * 1000))).slice(-2);
        let secs = ("0" + parseInt((milis - hours * 60 * 1000 * 60 - mins * 60 * 1000) / 1000)).slice(-2);
        return hours + ":" + mins + ":" + secs
    }

    render() {
        if (this.state.isOver) {
            return (
                <Alert color={"success"} className={"text-center"}>
                    <h3 className={"text-center"}>Our shop was closed</h3>
                </Alert>

            );
        } else {
            return (
                <Alert color={"primary"} className={"text-center"} style={{marginTop: "48px"}}>
                    <h3 className={"text-center"}>The current website is the scientific project on High Performance
                        Python Lab course in Skoltech. The using of this resource is not under the authors'
                        responsibility.</h3>
                    <br/>
                    <h3>This demo site will die in</h3>
                    <h3>{this.renderRemainingTime(this.state.milisecsRemaining)}</h3>
                </Alert>

            );
        }

    }

    componentDidMount() {
        let cur_date = new Date();
        let exp_date = new Date(2020, 11, 11, 10, 0, 0); // monthNum -1
        let milisecsRemaining = exp_date - cur_date;

        this.setState({
            expiration_date: exp_date,
            milisecsRemaining: exp_date - cur_date

        })


        if (milisecsRemaining < 900) {
            this.setState({isOver: true})

        }

        this.startTimer()
    }

    componentDidUpdate(prevState) {
        if (prevState.milisecsRemaining !== this.state.milisecsRemaining) {
        }
    }
}