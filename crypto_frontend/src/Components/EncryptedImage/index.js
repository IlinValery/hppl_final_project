import React from "react"
import './style.css'
import {Container, Row, Col, Form, FormGroup, Label, Input, Button} from 'reactstrap';
import Header from '../Header'
import './style.css'

export default class EncryptedImage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }
    render() {
        return (
            <Container fluid={true} className="page">
                <Row>
                    <Col>
                        <Header text={this.props.text}/>
                        <Button color="link">Download image</Button>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <Button color="secondary">Menu</Button>
                    </Col>
                </Row>
            </Container>
        );
    }
}