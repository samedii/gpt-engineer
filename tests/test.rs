use std::net::SocketAddr;
mod api;
mod database;
use api::router;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let app = router::router();

    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    tracing::debug!("listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
