import React from "react"
import './style.css'
import {Container, Row, Col, Form, FormGroup, Label, Input, Button} from 'reactstrap';
import Header from '../Header'
import './style.css'

export default class StartPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};

    }
    render() {
        return (
            <Container fluid={false} className="page">
                <Row>
                    <Col>
                        <Header text={this.props.text}/>
                    </Col>
                </Row>
                <Row>
                    <Button color="secondary">Encrypt</Button>{' '}
                </Row>
                <Row>
                    <Button color="secondary">
                        Decrypt
                    </Button>
                </Row>
            </Container>
        );
    }
}