import React from "react"
import './style.css'
import {Container, Row, Col, Form, FormGroup, Label, Input, Button} from 'reactstrap';

export default class Index extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};

    }
    render() {
        return (
            <Container fluid={false}>
                <Row>
                    <h1 className="header_text">{this.props.text}</h1>
                </Row>
            </Container>
        );
    }
}