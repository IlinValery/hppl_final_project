import React from "react"
import './style.css'

export default class Index extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};

    }
    render() {
        return (
            <div style={{paddingBottom: "48px"}}>
                <h1 className="header_text">{this.props.text}</h1>
            </div>
        );
    }
}