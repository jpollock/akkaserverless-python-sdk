const EventSourcedEntity = require("@lightbend/akkaserverless-python-sdk").EventSourcedEntity;
const entity = new EventSourcedEntity("shoppingcart.proto", "example.ShoppingCartService");
entity.setInitial(() => {});
entity.setBehavior(() => {
    return {
        commandHandlers: {},
        eventHandlers: {}
    };
});
module.exports = entity;


