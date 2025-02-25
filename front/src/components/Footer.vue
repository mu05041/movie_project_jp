<template>
  <footer class="text-center">
    <div class="container">
      <div class="footer-content">
        <div class="footer-brand">
          CINEBITE
        </div>
        <div class="footer-divider">|</div>
        <div class="footer-contact">
          CONTACT
          <span class="footer-email">contact@cinebite.com</span>
          <span class="footer-email">support@cinebite.com</span>
        </div>
        <div class="footer-divider">|</div>
        <div class="footer-social">
          SNS
          <div class="social-links">
            <a href="https://instagram.com" class="social-link">Instagram</a>
            <a href="https://twitter.com" class="social-link">Twitter</a>
          </div>
        </div>
      </div>
      <div class="footer-copyright">
        <P>© 2024 Cinebite. All rights reserved.</P>
        <P>Made By SAFFY</P>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
};
</script>

<style>
footer {
  background-color: var(--footer-bg);
  padding: 1.5rem 0;
  font-size: 0.75rem;
}

.footer-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 0.5rem;
}

.footer-brand {
  font-weight: 600;
  letter-spacing: 1px;
}

.footer-divider {
  color: rgba(0, 0, 0, 0.3);
}

.footer-contact {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.footer-email {
  color: rgba(0, 0, 0, 0.7);
  margin-left: 0.5rem;
}

.footer-social {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.social-links {
  display: flex;
  gap: 0.5rem;
  margin-left: 0.5rem;
}

.social-link {
  color: rgba(0, 0, 0, 0.7);
  text-decoration: none;
}

.social-link:hover {
  color: rgba(0, 0, 0, 0.9);
}

.footer-copyright {
  font-size: 0.7rem;
  color: rgba(0, 0, 0, 0.5);
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .footer-divider {
    display: none;
  }
  
  .footer-contact, .footer-social {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
